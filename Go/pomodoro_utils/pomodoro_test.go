package pomodoro_utils

import (
	"testing"
	"time"
)

func TestDefaultConfig(t *testing.T) {
	config := DefaultConfig()
	
	if config.WorkDuration != 25*time.Minute {
		t.Errorf("Expected work duration 25m, got %v", config.WorkDuration)
	}
	if config.ShortBreakDuration != 5*time.Minute {
		t.Errorf("Expected short break 5m, got %v", config.ShortBreakDuration)
	}
	if config.LongBreakDuration != 15*time.Minute {
		t.Errorf("Expected long break 15m, got %v", config.LongBreakDuration)
	}
	if config.SessionsUntilLongBreak != 4 {
		t.Errorf("Expected 4 sessions until long break, got %d", config.SessionsUntilLongBreak)
	}
}

func TestNewTimer(t *testing.T) {
	timer := NewTimerWithDefaults()
	
	if timer == nil {
		t.Fatal("Expected non-nil timer")
	}
	if timer.GetCurrentSessionType() != WorkSession {
		t.Errorf("Expected initial session type to be Work, got %v", timer.GetCurrentSessionType())
	}
	if timer.GetSessionNumber() != 1 {
		t.Errorf("Expected initial session number 1, got %d", timer.GetSessionNumber())
	}
}

func TestCustomConfig(t *testing.T) {
	config := Config{
		WorkDuration:           30 * time.Minute,
		ShortBreakDuration:     10 * time.Minute,
		LongBreakDuration:      20 * time.Minute,
		SessionsUntilLongBreak: 3,
	}
	timer := NewTimer(config)
	
	if timer.GetCurrentDuration() != 30*time.Minute {
		t.Errorf("Expected 30m duration, got %v", timer.GetCurrentDuration())
	}
}

func TestSessionTypeString(t *testing.T) {
	tests := []struct {
		st       SessionType
		expected string
	}{
		{WorkSession, "Work"},
		{ShortBreak, "Short Break"},
		{LongBreak, "Long Break"},
		{SessionType(99), "Unknown"},
	}
	
	for _, test := range tests {
		if result := test.st.String(); result != test.expected {
			t.Errorf("Expected %q, got %q", test.expected, result)
		}
	}
}

func TestAdvanceSession(t *testing.T) {
	timer := NewTimerWithDefaults()
	
	// Work -> Short Break
	timer.SkipSession()
	if timer.GetCurrentSessionType() != ShortBreak {
		t.Errorf("Expected ShortBreak after Work, got %v", timer.GetCurrentSessionType())
	}
	
	// Short Break -> Work (session 2)
	timer.SkipSession()
	if timer.GetCurrentSessionType() != WorkSession {
		t.Errorf("Expected Work after ShortBreak, got %v", timer.GetCurrentSessionType())
	}
	if timer.GetSessionNumber() != 2 {
		t.Errorf("Expected session 2, got %d", timer.GetSessionNumber())
	}
	
	// Progress through sessions
	timer.SkipSession() // Work -> ShortBreak
	timer.SkipSession() // ShortBreak -> Work (3)
	timer.SkipSession() // Work -> ShortBreak
	timer.SkipSession() // ShortBreak -> Work (4)
	
	if timer.GetSessionNumber() != 4 {
		t.Errorf("Expected session 4, got %d", timer.GetSessionNumber())
	}
	
	// Work (4) -> Long Break
	timer.SkipSession()
	if timer.GetCurrentSessionType() != LongBreak {
		t.Errorf("Expected LongBreak after 4th work session, got %v", timer.GetCurrentSessionType())
	}
	
	// Long Break -> Work (reset to session 1)
	timer.SkipSession()
	if timer.GetCurrentSessionType() != WorkSession {
		t.Errorf("Expected Work after LongBreak, got %v", timer.GetCurrentSessionType())
	}
	if timer.GetSessionNumber() != 1 {
		t.Errorf("Expected session 1 after long break, got %d", timer.GetSessionNumber())
	}
}

func TestReset(t *testing.T) {
	timer := NewTimerWithDefaults()
	
	// Advance through a few sessions
	timer.SkipSession()
	timer.SkipSession()
	timer.SkipSession()
	
	// Reset
	timer.Reset()
	
	if timer.GetCurrentSessionType() != WorkSession {
		t.Errorf("Expected Work after reset, got %v", timer.GetCurrentSessionType())
	}
	if timer.GetSessionNumber() != 1 {
		t.Errorf("Expected session 1 after reset, got %d", timer.GetSessionNumber())
	}
}

func TestFormatDuration(t *testing.T) {
	tests := []struct {
		duration time.Duration
		expected string
	}{
		{25 * time.Minute, "25m 0s"},
		{5 * time.Minute, "5m 0s"},
		{90 * time.Second, "1m 30s"},
		{30 * time.Second, "30s"},
		{2 * time.Hour, "2h 0m 0s"},
		{1*time.Hour + 30*time.Minute, "1h 30m 0s"},
	}
	
	for _, test := range tests {
		result := FormatDuration(test.duration)
		if result != test.expected {
			t.Errorf("For %v: expected %q, got %q", test.duration, test.expected, result)
		}
	}
}

func TestGetNextSessionType(t *testing.T) {
	timer := NewTimerWithDefaults()
	
	// Work -> ShortBreak
	if timer.GetNextSessionType() != ShortBreak {
		t.Errorf("Expected next to be ShortBreak, got %v", timer.GetNextSessionType())
	}
	
	timer.SkipSession()
	// ShortBreak -> Work
	if timer.GetNextSessionType() != WorkSession {
		t.Errorf("Expected next to be Work, got %v", timer.GetNextSessionType())
	}
}

func TestGetProgress(t *testing.T) {
	timer := NewTimerWithDefaults()
	
	current, total := timer.GetProgress()
	if current != 1 || total != 4 {
		t.Errorf("Expected progress 1/4, got %d/%d", current, total)
	}
	
	timer.SkipSession()
	timer.SkipSession()
	
	current, total = timer.GetProgress()
	if current != 2 || total != 4 {
		t.Errorf("Expected progress 2/4, got %d/%d", current, total)
	}
}

func TestCalculateProductivityScore(t *testing.T) {
	timer := NewTimerWithDefaults()
	
	// No sessions
	if score := timer.CalculateProductivityScore(); score != 0 {
		t.Errorf("Expected score 0 with no sessions, got %f", score)
	}
}

func TestPredictEndTime(t *testing.T) {
	timer := NewTimerWithDefaults()
	
	// Predict end time for 1 session (25m)
	endTime := timer.PredictEndTime(1)
	expected := time.Now().Add(25 * time.Minute)
	diff := endTime.Sub(expected)
	if diff < 0 {
		diff = -diff
	}
	if diff > time.Second {
		t.Errorf("Predicted time off by more than 1s: %v", diff)
	}
	
	// Predict for 4 sessions (4 work + 3 short breaks)
	// 4*25m + 3*5m = 100m + 15m = 115m
	endTime = timer.PredictEndTime(4)
	expected = time.Now().Add(115 * time.Minute)
	diff = endTime.Sub(expected)
	if diff < 0 {
		diff = -diff
	}
	if diff > time.Second {
		t.Errorf("Predicted time off by more than 1s: %v", diff)
	}
}

func TestStartSession(t *testing.T) {
	timer := NewTimerWithDefaults()
	
	// Use a very short duration for testing
	testConfig := Config{
		WorkDuration:           100 * time.Millisecond,
		ShortBreakDuration:     50 * time.Millisecond,
		LongBreakDuration:      150 * time.Millisecond,
		SessionsUntilLongBreak: 4,
	}
	timer.SetConfig(testConfig)
	
	endTime, done := timer.StartSession()
	
	if endTime.IsZero() {
		t.Error("Expected non-zero end time")
	}
	
	// Wait for session to complete
	select {
	case <-done:
		stats := timer.GetStats()
		if stats.TotalWorkSessions != 1 {
			t.Errorf("Expected 1 work session, got %d", stats.TotalWorkSessions)
		}
		if stats.CurrentStreak != 1 {
			t.Errorf("Expected streak 1, got %d", stats.CurrentStreak)
		}
	case <-time.After(time.Second):
		t.Error("Session did not complete in time")
	}
	
	// After work session, should be on break
	if timer.GetCurrentSessionType() != ShortBreak {
		t.Errorf("Expected ShortBreak after work, got %v", timer.GetCurrentSessionType())
	}
}

func TestBreakStreak(t *testing.T) {
	timer := NewTimerWithDefaults()
	
	// Simulate some streak
	timer.mu.Lock()
	timer.stats.CurrentStreak = 5
	timer.stats.LongestStreak = 5
	timer.mu.Unlock()
	
	timer.BreakStreak()
	
	stats := timer.GetStats()
	if stats.CurrentStreak != 0 {
		t.Errorf("Expected streak 0, got %d", stats.CurrentStreak)
	}
	// Longest streak should remain
	if stats.LongestStreak != 5 {
		t.Errorf("Expected longest streak to remain 5, got %d", stats.LongestStreak)
	}
}

func TestResetStats(t *testing.T) {
	timer := NewTimerWithDefaults()
	
	// Add some stats
	timer.mu.Lock()
	timer.stats.TotalWorkSessions = 10
	timer.stats.CurrentStreak = 5
	timer.mu.Unlock()
	
	timer.ResetStats()
	
	stats := timer.GetStats()
	if stats.TotalWorkSessions != 0 {
		t.Errorf("Expected 0 sessions, got %d", stats.TotalWorkSessions)
	}
	if stats.CurrentStreak != 0 {
		t.Errorf("Expected 0 streak, got %d", stats.CurrentStreak)
	}
}

func TestGetDailyGoalProgress(t *testing.T) {
	timer := NewTimerWithDefaults()
	
	// Add some sessions for today
	now := time.Now()
	timer.mu.Lock()
	timer.sessions = append(timer.sessions,
		Session{Type: WorkSession, StartTime: now.Add(-2 * time.Hour)},
		Session{Type: WorkSession, StartTime: now.Add(-1 * time.Hour)},
	)
	timer.stats.TotalWorkSessions = 2
	timer.mu.Unlock()
	
	completed, goal, percentage := timer.GetDailyGoalProgress(8)
	
	if completed != 2 {
		t.Errorf("Expected 2 completed, got %d", completed)
	}
	if goal != 8 {
		t.Errorf("Expected goal 8, got %d", goal)
	}
	if percentage != 25.0 {
		t.Errorf("Expected 25%%, got %f%%", percentage)
	}
}

func TestSummary(t *testing.T) {
	timer := NewTimerWithDefaults()
	summary := timer.Summary()
	
	if summary == "" {
		t.Error("Expected non-empty summary")
	}
	
	// Should contain key info
	if !containsStr(summary, "Work") {
		t.Error("Summary should contain 'Work'")
	}
	if !containsStr(summary, "Session") {
		t.Error("Summary should contain 'Session'")
	}
}

func containsStr(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(s) > 0 && containsStr(s[1:], substr) || s[:len(substr)] == substr)
}

func TestGetConfig(t *testing.T) {
	customConfig := Config{
		WorkDuration:           50 * time.Minute,
		ShortBreakDuration:     10 * time.Minute,
		LongBreakDuration:      30 * time.Minute,
		SessionsUntilLongBreak: 2,
	}
	timer := NewTimer(customConfig)
	
	config := timer.GetConfig()
	if config.WorkDuration != 50*time.Minute {
		t.Errorf("Expected 50m work duration, got %v", config.WorkDuration)
	}
	if config.SessionsUntilLongBreak != 2 {
		t.Errorf("Expected 2 sessions until long break, got %d", config.SessionsUntilLongBreak)
	}
}

func TestGetSessions(t *testing.T) {
	timer := NewTimerWithDefaults()
	now := time.Now()
	
	timer.mu.Lock()
	timer.sessions = append(timer.sessions,
		Session{Type: WorkSession, StartTime: now, EndTime: now.Add(25 * time.Minute)},
		Session{Type: ShortBreak, StartTime: now.Add(26 * time.Minute), EndTime: now.Add(31 * time.Minute)},
	)
	timer.mu.Unlock()
	
	sessions := timer.GetSessions()
	if len(sessions) != 2 {
		t.Errorf("Expected 2 sessions, got %d", len(sessions))
	}
}

func TestConcurrentAccess(t *testing.T) {
	timer := NewTimerWithDefaults()
	done := make(chan bool)
	
	// Concurrent reads
	for i := 0; i < 10; i++ {
		go func() {
			for j := 0; j < 100; j++ {
				_ = timer.GetCurrentSessionType()
				_ = timer.GetStats()
				_, _ = timer.GetProgress()
			}
			done <- true
		}()
	}
	
	// Concurrent writes
	for i := 0; i < 5; i++ {
		go func() {
			for j := 0; j < 50; j++ {
				timer.SkipSession()
				timer.BreakStreak()
			}
			done <- true
		}()
	}
	
	// Wait for all goroutines
	for i := 0; i < 15; i++ {
		<-done
	}
}

func TestGetCurrentDuration(t *testing.T) {
	timer := NewTimerWithDefaults()
	
	// Work session
	if duration := timer.GetCurrentDuration(); duration != 25*time.Minute {
		t.Errorf("Expected 25m for work, got %v", duration)
	}
	
	timer.SkipSession()
	// Short break
	if duration := timer.GetCurrentDuration(); duration != 5*time.Minute {
		t.Errorf("Expected 5m for short break, got %v", duration)
	}
}

// Benchmark tests
func BenchmarkSkipSession(b *testing.B) {
	timer := NewTimerWithDefaults()
	for i := 0; i < b.N; i++ {
		timer.SkipSession()
	}
}

func BenchmarkGetStats(b *testing.B) {
	timer := NewTimerWithDefaults()
	for i := 0; i < b.N; i++ {
		_ = timer.GetStats()
	}
}

func BenchmarkCalculateProductivityScore(b *testing.B) {
	timer := NewTimerWithDefaults()
	for i := 0; i < b.N; i++ {
		_ = timer.CalculateProductivityScore()
	}
}