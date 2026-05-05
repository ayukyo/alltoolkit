// Package progressbar provides a simple, zero-dependency progress bar for CLI applications.
package progressbar

import (
	"fmt"
	"io"
	"os"
	"strings"
	"sync"
	"time"
)

// ProgressBar represents a customizable progress bar
type ProgressBar struct {
	total     int64
	current   int64
	width     int
	complete  string
	incomplete string
	writer    io.Writer
	mu        sync.Mutex
	startTime time.Time
	showSpeed bool
	showETA   bool
	prefix    string
	suffix    string
}

// Option is a functional option for configuring ProgressBar
type Option func(*ProgressBar)

// WithWidth sets the width of the progress bar
func WithWidth(width int) Option {
	return func(pb *ProgressBar) {
		if width > 0 {
			pb.width = width
		}
	}
}

// WithCompleteChar sets the character for completed portion
func WithCompleteChar(char string) Option {
	return func(pb *ProgressBar) {
		if char != "" {
			pb.complete = char
		}
	}
}

// WithIncompleteChar sets the character for incomplete portion
func WithIncompleteChar(char string) Option {
	return func(pb *ProgressBar) {
		if char != "" {
			pb.incomplete = char
		}
	}
}

// WithWriter sets the output writer
func WithWriter(w io.Writer) Option {
	return func(pb *ProgressBar) {
		if w != nil {
			pb.writer = w
		}
	}
}

// WithSpeed enables/disables speed display
func WithSpeed(show bool) Option {
	return func(pb *ProgressBar) {
		pb.showSpeed = show
	}
}

// WithETA enables/disables ETA display
func WithETA(show bool) Option {
	return func(pb *ProgressBar) {
		pb.showETA = show
	}
}

// WithPrefix sets a prefix string
func WithPrefix(prefix string) Option {
	return func(pb *ProgressBar) {
		pb.prefix = prefix
	}
}

// WithSuffix sets a suffix string
func WithSuffix(suffix string) Option {
	return func(pb *ProgressBar) {
		pb.suffix = suffix
	}
}

// New creates a new ProgressBar with the given total
func New(total int64, opts ...Option) *ProgressBar {
	pb := &ProgressBar{
		total:     total,
		current:   0,
		width:     40,
		complete:  "█",
		incomplete: "░",
		writer:    os.Stdout,
		startTime: time.Now(),
		showSpeed: false,
		showETA:   false,
		prefix:    "",
		suffix:    "",
	}

	for _, opt := range opts {
		opt(pb)
	}

	return pb
}

// Add increments the progress by n
func (pb *ProgressBar) Add(n int64) {
	pb.mu.Lock()
	defer pb.mu.Unlock()
	pb.current += n
	if pb.current > pb.total {
		pb.current = pb.total
	}
}

// Set sets the current progress to n
func (pb *ProgressBar) Set(n int64) {
	pb.mu.Lock()
	defer pb.mu.Unlock()
	if n > pb.total {
		pb.current = pb.total
	} else if n < 0 {
		pb.current = 0
	} else {
		pb.current = n
	}
}

// Increment increments the progress by 1
func (pb *ProgressBar) Increment() {
	pb.Add(1)
}

// Render renders the progress bar to the writer
func (pb *ProgressBar) Render() {
	pb.mu.Lock()
	defer pb.mu.Unlock()

	var sb strings.Builder

	// Calculate percentage
	percent := float64(0)
	if pb.total > 0 {
		percent = float64(pb.current) / float64(pb.total) * 100
	}

	// Build prefix
	if pb.prefix != "" {
		sb.WriteString(pb.prefix)
		sb.WriteString(" ")
	}

	// Build progress bar
	completeWidth := int(float64(pb.width) * percent / 100)
	incompleteWidth := pb.width - completeWidth

	sb.WriteString("[")
	sb.WriteString(strings.Repeat(pb.complete, completeWidth))
	sb.WriteString(strings.Repeat(pb.incomplete, incompleteWidth))
	sb.WriteString("]")

	// Build percentage
	sb.WriteString(fmt.Sprintf(" %.1f%%", percent))

	// Build counter
	sb.WriteString(fmt.Sprintf(" (%d/%d)", pb.current, pb.total))

	// Build speed
	if pb.showSpeed && pb.current > 0 {
		elapsed := time.Since(pb.startTime).Seconds()
		if elapsed > 0 {
			speed := float64(pb.current) / elapsed
			sb.WriteString(fmt.Sprintf(" [%s/s]", formatSpeed(speed)))
		}
	}

	// Build ETA
	if pb.showETA && pb.current > 0 && pb.current < pb.total {
		elapsed := time.Since(pb.startTime).Seconds()
		if elapsed > 0 && pb.current > 0 {
			rate := float64(pb.current) / elapsed
			if rate > 0 {
				remaining := float64(pb.total-pb.current) / rate
				sb.WriteString(fmt.Sprintf(" [ETA: %s]", formatDuration(time.Duration(remaining)*time.Second)))
			}
		}
	}

	// Build suffix
	if pb.suffix != "" {
		sb.WriteString(" ")
		sb.WriteString(pb.suffix)
	}

	// Clear line and write
	fmt.Fprintf(pb.writer, "\r%s", sb.String())
}

// Renderln renders the progress bar with a newline
func (pb *ProgressBar) Renderln() {
	pb.Render()
	fmt.Fprintln(pb.writer)
}

// Reset resets the progress bar
func (pb *ProgressBar) Reset() {
	pb.mu.Lock()
	defer pb.mu.Unlock()
	pb.current = 0
	pb.startTime = time.Now()
}

// Finish completes the progress bar and prints a newline
func (pb *ProgressBar) Finish() {
	pb.Set(pb.total)
	pb.Render()
	fmt.Fprintln(pb.writer)
}

// IsComplete returns true if the progress is complete
func (pb *ProgressBar) IsComplete() bool {
	pb.mu.Lock()
	defer pb.mu.Unlock()
	return pb.current >= pb.total
}

// Percentage returns the current percentage
func (pb *ProgressBar) Percentage() float64 {
	pb.mu.Lock()
	defer pb.mu.Unlock()
	if pb.total == 0 {
		return 0
	}
	return float64(pb.current) / float64(pb.total) * 100
}

// Elapsed returns the elapsed time
func (pb *ProgressBar) Elapsed() time.Duration {
	return time.Since(pb.startTime)
}

// Current returns the current progress
func (pb *ProgressBar) Current() int64 {
	pb.mu.Lock()
	defer pb.mu.Unlock()
	return pb.current
}

// Total returns the total
func (pb *ProgressBar) Total() int64 {
	return pb.total
}

// formatSpeed formats speed with appropriate unit
func formatSpeed(speed float64) string {
	units := []string{"B", "KB", "MB", "GB", "TB"}
	unitIndex := 0

	for speed >= 1024 && unitIndex < len(units)-1 {
		speed /= 1024
		unitIndex++
	}

	return fmt.Sprintf("%.2f%s", speed, units[unitIndex])
}

// formatDuration formats duration in a human-readable way
func formatDuration(d time.Duration) string {
	if d < time.Second {
		return "0s"
	}

	seconds := int(d.Seconds()) % 60
	minutes := int(d.Minutes()) % 60
	hours := int(d.Hours())

	if hours > 0 {
		return fmt.Sprintf("%dh %dm %ds", hours, minutes, seconds)
	}
	if minutes > 0 {
		return fmt.Sprintf("%dm %ds", minutes, seconds)
	}
	return fmt.Sprintf("%ds", seconds)
}

// Spinner represents an animated spinner
type Spinner struct {
	frames  []string
	current int
	writer  io.Writer
	mu      sync.Mutex
	prefix  string
	suffix  string
}

// SpinnerOption is a functional option for configuring Spinner
type SpinnerOption func(*Spinner)

// WithSpinnerFrames sets custom frames
func WithSpinnerFrames(frames []string) SpinnerOption {
	return func(s *Spinner) {
		if len(frames) > 0 {
			s.frames = frames
		}
	}
}

// WithSpinnerPrefix sets the prefix
func WithSpinnerPrefix(prefix string) SpinnerOption {
	return func(s *Spinner) {
		s.prefix = prefix
	}
}

// WithSpinnerSuffix sets the suffix
func WithSpinnerSuffix(suffix string) SpinnerOption {
	return func(s *Spinner) {
		s.suffix = suffix
	}
}

// WithSpinnerWriter sets the output writer
func WithSpinnerWriter(w io.Writer) SpinnerOption {
	return func(s *Spinner) {
		if w != nil {
			s.writer = w
		}
	}
}

// NewSpinner creates a new spinner
func NewSpinner(opts ...SpinnerOption) *Spinner {
	s := &Spinner{
		frames: []string{"⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"},
		writer: os.Stdout,
		prefix: "",
		suffix: "",
	}

	for _, opt := range opts {
		opt(s)
	}

	return s
}

// Next advances to the next frame
func (s *Spinner) Next() {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.current = (s.current + 1) % len(s.frames)
}

// Render renders the current spinner frame
func (s *Spinner) Render() {
	s.mu.Lock()
	defer s.mu.Unlock()
	fmt.Fprintf(s.writer, "\r%s%s%s", s.prefix, s.frames[s.current], s.suffix)
}

// Clear clears the spinner line
func (s *Spinner) Clear() {
	s.mu.Lock()
	defer s.mu.Unlock()
	fmt.Fprintf(s.writer, "\r%s\r", strings.Repeat(" ", len(s.prefix)+len(s.suffix)+10))
}

// MultiBar manages multiple progress bars
type MultiBar struct {
	bars   []*ProgressBar
	writer io.Writer
	mu     sync.Mutex
}

// NewMultiBar creates a new MultiBar
func NewMultiBar() *MultiBar {
	return &MultiBar{
		bars:   make([]*ProgressBar, 0),
		writer: os.Stdout,
	}
}

// Add adds a new progress bar
func (mb *MultiBar) Add(total int64, opts ...Option) *ProgressBar {
	mb.mu.Lock()
	defer mb.mu.Unlock()
	
	// Create with index prefix
	opts = append(opts, WithPrefix(fmt.Sprintf("[%d]", len(mb.bars)+1)))
	pb := New(total, opts...)
	mb.bars = append(mb.bars, pb)
	return pb
}

// RenderAll renders all progress bars
func (mb *MultiBar) RenderAll() {
	mb.mu.Lock()
	defer mb.mu.Unlock()

	// Move cursor up for each bar
	if len(mb.bars) > 0 {
		for i := len(mb.bars) - 1; i >= 0; i-- {
			fmt.Fprint(mb.writer, "\033[F") // Move cursor up one line
		}
	}

	// Render all bars
	for _, pb := range mb.bars {
		pb.Render()
		fmt.Fprintln(mb.writer)
	}
}

// Countdown represents a countdown timer
type Countdown struct {
	duration time.Duration
	writer   io.Writer
	prefix   string
}

// CountdownOption is a functional option for configuring Countdown
type CountdownOption func(*Countdown)

// WithCountdownPrefix sets the prefix
func WithCountdownPrefix(prefix string) CountdownOption {
	return func(c *Countdown) {
		c.prefix = prefix
	}
}

// WithCountdownWriter sets the output writer
func WithCountdownWriter(w io.Writer) CountdownOption {
	return func(c *Countdown) {
		if w != nil {
			c.writer = w
		}
	}
}

// NewCountdown creates a new countdown
func NewCountdown(duration time.Duration, opts ...CountdownOption) *Countdown {
	c := &Countdown{
		duration: duration,
		writer:   os.Stdout,
		prefix:   "",
	}

	for _, opt := range opts {
		opt(c)
	}

	return c
}

// Start starts the countdown and blocks until complete
func (c *Countdown) Start() {
	end := time.Now().Add(c.duration)
	ticker := time.NewTicker(time.Second)
	defer ticker.Stop()

	for range ticker.C {
		remaining := time.Until(end)
		if remaining <= 0 {
			fmt.Fprintf(c.writer, "\r%s00:00:00\n", c.prefix)
			return
		}

		hours := int(remaining.Hours())
		minutes := int(remaining.Minutes()) % 60
		seconds := int(remaining.Seconds()) % 60

		fmt.Fprintf(c.writer, "\r%s%02d:%02d:%02d", c.prefix, hours, minutes, seconds)
	}
}