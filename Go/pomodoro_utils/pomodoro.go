// Package pomodoro_utils provides a Pomodoro timer implementation for time management.
// It supports customizable work/break durations, session tracking, and statistics.
package pomodoro_utils

import (
	"fmt"
	"sync"
	"time"
)

// SessionType represents the type of pomodoro session
type SessionType int

const (
	WorkSession SessionType = iota
	ShortBreak
	LongBreak
)

// String returns the string representation of SessionType
func (st SessionType) String() string {
	switch st {
	case WorkSession:
		return "Work"
	case ShortBreak:
		return "Short Break"
	case LongBreak:
		return "Long Break"
	default:
		return "Unknown"
	}
}

// Config holds the pomodoro timer configuration
type Config struct {
	WorkDuration       time.Duration // Duration of work sessions
	ShortBreakDuration time.Duration // Duration of short breaks
	LongBreakDuration  time.Duration // Duration of long breaks
	SessionsUntilLongBreak int       // Number of work sessions before a long break
}

// DefaultConfig returns the standard Pomodoro configuration (25/5/15)
func DefaultConfig() Config {
	return Config{
		WorkDuration:           25 * time.Minute,
		ShortBreakDuration:     5 * time.Minute,
		LongBreakDuration:      15 * time.Minute,
		SessionsUntilLongBreak: 4,
	}
}

// Stats holds statistics about completed sessions
type Stats struct {
	TotalWorkSessions   int           `json:"total_work_sessions"`
	TotalBreaks         int           `json:"total_breaks"`
	TotalWorkTime       time.Duration `json:"total_work_time"`
	TotalBreakTime      time.Duration `json:"total_break_time"`
	LongestStreak       int           `json:"longest_streak"`
	CurrentStreak       int           `json:"current_streak"`
	LastSessionComplete time.Time     `json:"last_session_complete"`
}

// Session represents a completed session record
type Session struct {
	Type      SessionType  `json:"type"`
	Duration  time.Duration `json:"duration"`
	StartTime time.Time     `json:"start_time"`
	EndTime   time.Time     `json:"end_time"`
}

// Timer represents a Pomodoro timer
type Timer struct {
	config      Config
	stats       Stats
	sessions    []Session
	mu          sync.RWMutex
	currentType SessionType
	sessionNum  int // Current session number in the cycle
}

// NewTimer creates a new Pomodoro timer with the given configuration
func NewTimer(config Config) *Timer {
	return &Timer{
		config:     config,
		sessions:   make([]Session, 0),
		currentType: WorkSession,
		sessionNum: 1,
	}
}

// NewTimerWithDefaults creates a new Pomodoro timer with default configuration
func NewTimerWithDefaults() *Timer {
	return NewTimer(DefaultConfig())
}

// GetCurrentSessionType returns the type of the current session
func (t *Timer) GetCurrentSessionType() SessionType {
	t.mu.RLock()
	defer t.mu.RUnlock()
	return t.currentType
}

// GetCurrentDuration returns the duration of the current session type
func (t *Timer) GetCurrentDuration() time.Duration {
	t.mu.RLock()
	defer t.mu.RUnlock()
	return t.getDurationForType(t.currentType)
}

// getDurationForType returns the duration for a given session type
func (t *Timer) getDurationForType(st SessionType) time.Duration {
	switch st {
	case WorkSession:
		return t.config.WorkDuration
	case ShortBreak:
		return t.config.ShortBreakDuration
	case LongBreak:
		return t.config.LongBreakDuration
	default:
		return 0
	}
}

// GetSessionNumber returns the current session number in the cycle
func (t *Timer) GetSessionNumber() int {
	t.mu.RLock()
	defer t.mu.RUnlock()
	return t.sessionNum
}

// StartSession starts a session and returns a channel that will receive when done
// Returns the end time and a channel that closes when the session completes
func (t *Timer) StartSession() (time.Time, <-chan time.Time) {
	done := make(chan time.Time)
	
	t.mu.Lock()
	duration := t.getDurationForType(t.currentType)
	sessionType := t.currentType
	startTime := time.Now()
	endTime := startTime.Add(duration)
	t.mu.Unlock()

	go func() {
		timer := time.NewTimer(duration)
		<-timer.C
		
		t.mu.Lock()
		defer t.mu.Unlock()
		
		// Record the session
		session := Session{
			Type:      sessionType,
			Duration:  duration,
			StartTime: startTime,
			EndTime:   time.Now(),
		}
		t.sessions = append(t.sessions, session)
		
		// Update stats
		if sessionType == WorkSession {
			t.stats.TotalWorkSessions++
			t.stats.TotalWorkTime += duration
			t.stats.CurrentStreak++
			if t.stats.CurrentStreak > t.stats.LongestStreak {
				t.stats.LongestStreak = t.stats.CurrentStreak
			}
		} else {
			t.stats.TotalBreaks++
			t.stats.TotalBreakTime += duration
		}
		t.stats.LastSessionComplete = time.Now()
		
		// Advance to next session type
		t.advanceSession()
		
		close(done)
	}()

	return endTime, done
}

// advanceSession moves to the next session type (must be called with lock held)
func (t *Timer) advanceSession() {
	if t.currentType == WorkSession {
		// After work, check if we need a long break
		if t.sessionNum >= t.config.SessionsUntilLongBreak {
			t.currentType = LongBreak
			// sessionNum will be reset after long break
		} else {
			t.currentType = ShortBreak
			// sessionNum stays the same during break
		}
	} else if t.currentType == ShortBreak {
		// After short break, go back to work with incremented session number
		t.currentType = WorkSession
		t.sessionNum++
	} else {
		// After long break, start fresh with session 1
		t.currentType = WorkSession
		t.sessionNum = 1
	}
}

// SkipSession skips the current session and moves to the next
func (t *Timer) SkipSession() {
	t.mu.Lock()
	defer t.mu.Unlock()
	t.advanceSession()
}

// Reset resets the timer to initial state
func (t *Timer) Reset() {
	t.mu.Lock()
	defer t.mu.Unlock()
	t.currentType = WorkSession
	t.sessionNum = 1
}

// ResetStats resets all statistics
func (t *Timer) ResetStats() {
	t.mu.Lock()
	defer t.mu.Unlock()
	t.stats = Stats{}
	t.sessions = make([]Session, 0)
}

// GetStats returns the current statistics
func (t *Timer) GetStats() Stats {
	t.mu.RLock()
	defer t.mu.RUnlock()
	return t.stats
}

// GetSessions returns all completed sessions
func (t *Timer) GetSessions() []Session {
	t.mu.RLock()
	defer t.mu.RUnlock()
	result := make([]Session, len(t.sessions))
	copy(result, t.sessions)
	return result
}

// GetConfig returns the current configuration
func (t *Timer) GetConfig() Config {
	t.mu.RLock()
	defer t.mu.RUnlock()
	return t.config
}

// SetConfig updates the timer configuration
func (t *Timer) SetConfig(config Config) {
	t.mu.Lock()
	defer t.mu.Unlock()
	t.config = config
}

// BreakStreak resets the current streak (call when user misses a session)
func (t *Timer) BreakStreak() {
	t.mu.Lock()
	defer t.mu.Unlock()
	t.stats.CurrentStreak = 0
}

// FormatDuration formats a duration in a human-readable way
func FormatDuration(d time.Duration) string {
	hours := int(d.Hours())
	minutes := int(d.Minutes()) % 60
	seconds := int(d.Seconds()) % 60
	
	if hours > 0 {
		return fmt.Sprintf("%dh %dm %ds", hours, minutes, seconds)
	}
	if minutes > 0 {
		return fmt.Sprintf("%dm %ds", minutes, seconds)
	}
	return fmt.Sprintf("%ds", seconds)
}

// GetNextSessionType returns what the next session type will be
func (t *Timer) GetNextSessionType() SessionType {
	t.mu.RLock()
	defer t.mu.RUnlock()
	
	if t.currentType == WorkSession {
		if t.sessionNum >= t.config.SessionsUntilLongBreak {
			return LongBreak
		}
		return ShortBreak
	}
	return WorkSession
}

// GetProgress returns the progress within the current pomodoro cycle
// Returns (current work session, total sessions before long break)
func (t *Timer) GetProgress() (int, int) {
	t.mu.RLock()
	defer t.mu.RUnlock()
	return t.sessionNum, t.config.SessionsUntilLongBreak
}

// PredictEndTime predicts when all sessions will end if following the standard cycle
func (t *Timer) PredictEndTime(sessions int) time.Time {
	t.mu.RLock()
	defer t.mu.RUnlock()
	
	if sessions <= 0 {
		return time.Now()
	}
	
	var total time.Duration
	for i := 0; i < sessions; i++ {
		total += t.config.WorkDuration
		// Add break after each work session except the last
		if i < sessions-1 {
			if (i+1)%t.config.SessionsUntilLongBreak == 0 {
				total += t.config.LongBreakDuration
			} else {
				total += t.config.ShortBreakDuration
			}
		}
	}
	
	return time.Now().Add(total)
}

// CalculateProductivityScore returns a productivity score based on completed sessions
// Score is based on total work time and streak bonus
func (t *Timer) CalculateProductivityScore() float64 {
	t.mu.RLock()
	defer t.mu.RUnlock()
	
	if t.stats.TotalWorkSessions == 0 {
		return 0
	}
	
	// Base score: 10 points per completed work session
	baseScore := float64(t.stats.TotalWorkSessions) * 10
	
	// Streak bonus: up to 50% bonus based on longest streak
	streakBonus := float64(t.stats.LongestStreak) * 2
	
	// Consistency bonus: bonus for maintaining current streak
	consistencyBonus := float64(t.stats.CurrentStreak) * 0.5
	
	return baseScore + streakBonus + consistencyBonus
}

// GetDailyGoalProgress calculates progress toward a daily work goal
// Returns (completed sessions, goal sessions, percentage)
func (t *Timer) GetDailyGoalProgress(dailyGoal int) (int, int, float64) {
	t.mu.RLock()
	defer t.mu.RUnlock()
	
	today := time.Now().Format("2006-01-02")
	todaySessions := 0
	
	for _, s := range t.sessions {
		if s.Type == WorkSession && s.StartTime.Format("2006-01-02") == today {
			todaySessions++
		}
	}
	
	percentage := 0.0
	if dailyGoal > 0 {
		percentage = float64(todaySessions) / float64(dailyGoal) * 100
		if percentage > 100 {
			percentage = 100
		}
	}
	
	return todaySessions, dailyGoal, percentage
}

// Summary returns a string summary of the timer state
func (t *Timer) Summary() string {
	t.mu.RLock()
	defer t.mu.RUnlock()
	
	return fmt.Sprintf(
		"Pomodoro Timer Summary:\n"+
			"  Current Session: %s #%d\n"+
			"  Duration: %s\n"+
			"  Total Work Sessions: %d\n"+
			"  Total Work Time: %s\n"+
			"  Current Streak: %d\n"+
			"  Longest Streak: %d\n"+
			"  Productivity Score: %.1f",
		t.currentType, t.sessionNum,
		FormatDuration(t.getDurationForType(t.currentType)),
		t.stats.TotalWorkSessions,
		FormatDuration(t.stats.TotalWorkTime),
		t.stats.CurrentStreak,
		t.stats.LongestStreak,
		t.CalculateProductivityScore(),
	)
}