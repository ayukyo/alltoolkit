// Example usage of the pomodoro_utils package
package main

import (
	"fmt"
	"time"

	"github.com/ayukyo/alltoolkit/Go/pomodoro_utils"
)

func main() {
	fmt.Println("🍅 Pomodoro Timer Example")
	fmt.Println("========================")
	fmt.Println()

	// Example 1: Basic usage with default configuration
	fmt.Println("Example 1: Basic Timer Setup")
	fmt.Println("----------------------------")
	timer := pomodoro_utils.NewTimerWithDefaults()
	fmt.Println(timer.Summary())
	fmt.Println()

	// Example 2: Custom configuration
	fmt.Println("Example 2: Custom Configuration (50/10/30)")
	fmt.Println("-------------------------------------------")
	customConfig := pomodoro_utils.Config{
		WorkDuration:           50 * time.Minute,
		ShortBreakDuration:     10 * time.Minute,
		LongBreakDuration:      30 * time.Minute,
		SessionsUntilLongBreak: 3,
	}
	customTimer := pomodoro_utils.NewTimer(customConfig)
	fmt.Printf("Work Duration: %s\n", pomodoro_utils.FormatDuration(customTimer.GetCurrentDuration()))
	fmt.Printf("Sessions until long break: %d\n\n", customConfig.SessionsUntilLongBreak)

	// Example 3: Simulating session progression
	fmt.Println("Example 3: Session Progression Simulation")
	fmt.Println("-----------------------------------------")
	timer2 := pomodoro_utils.NewTimerWithDefaults()
	
	for i := 1; i <= 6; i++ {
		current, total := timer2.GetProgress()
		sessionType := timer2.GetCurrentSessionType()
		duration := timer2.GetCurrentDuration()
		
		fmt.Printf("Step %d: %s", i, sessionType)
		if sessionType == pomodoro_utils.WorkSession {
			fmt.Printf(" (Session %d/%d)", current, total)
		}
		fmt.Printf(" - %s\n", pomodoro_utils.FormatDuration(duration))
		
		timer2.SkipSession()
	}
	fmt.Println()

	// Example 4: Statistics and productivity
	fmt.Println("Example 4: Statistics Tracking")
	fmt.Println("------------------------------")
	statsTimer := pomodoro_utils.NewTimerWithDefaults()
	
	// Simulate completed work
	statsTimer.SkipSession() // Work -> ShortBreak
	statsTimer.SkipSession() // ShortBreak -> Work 2
	statsTimer.SkipSession() // Work 2 -> ShortBreak
	statsTimer.SkipSession() // ShortBreak -> Work 3
	
	stats := statsTimer.GetStats()
	fmt.Printf("Sessions Completed: %d\n", stats.TotalWorkSessions)
	fmt.Printf("Current Streak: %d\n", stats.CurrentStreak)
	fmt.Printf("Productivity Score: %.1f\n", statsTimer.CalculateProductivityScore())
	fmt.Println()

	// Example 5: Daily goal progress
	fmt.Println("Example 5: Daily Goal Progress")
	fmt.Println("------------------------------")
	dailyGoal := 8
	completed, goal, percentage := statsTimer.GetDailyGoalProgress(dailyGoal)
	fmt.Printf("Daily Goal: %d pomodoros\n", goal)
	fmt.Printf("Completed: %d\n", completed)
	fmt.Printf("Progress: %.0f%%\n", percentage)
	
	progressBar := generateProgressBar(percentage, 20)
	fmt.Printf("[%s] %.0f%%\n\n", progressBar, percentage)

	// Example 6: Predict end time for work sessions
	fmt.Println("Example 6: Time Prediction")
	fmt.Println("--------------------------")
	workSessions := 4
	endTime := statsTimer.PredictEndTime(workSessions)
	fmt.Printf("If you start now and complete %d work sessions:\n", workSessions)
	fmt.Printf("Estimated finish time: %s\n", endTime.Format("3:04 PM"))
	
	totalDuration := 4*25*time.Minute + 3*5*time.Minute // 4 work + 3 short breaks
	fmt.Printf("Total time needed: %s\n\n", pomodoro_utils.FormatDuration(totalDuration))

	// Example 7: Format Duration utility
	fmt.Println("Example 7: Duration Formatting")
	fmt.Println("------------------------------")
	durations := []time.Duration{
		25 * time.Minute,
		5 * time.Minute,
		15 * time.Minute,
		2 * time.Hour,
		1*time.Hour + 30*time.Minute + 45*time.Second,
	}
	
	for _, d := range durations {
		fmt.Printf("%v -> %s\n", d, pomodoro_utils.FormatDuration(d))
	}
	fmt.Println()

	// Example 8: Different session types
	fmt.Println("Example 8: Session Types")
	fmt.Println("-----------------------")
	sessionTypes := []pomodoro_utils.SessionType{
		pomodoro_utils.WorkSession,
		pomodoro_utils.ShortBreak,
		pomodoro_utils.LongBreak,
	}
	
	for _, st := range sessionTypes {
		fmt.Printf("- %s\n", st.String())
	}
	fmt.Println()

	// Example 9: Quick timer test (very short)
	fmt.Println("Example 9: Live Timer Demo (100ms work session)")
	fmt.Println("-------------------------------------------------")
	testConfig := pomodoro_utils.Config{
		WorkDuration:           100 * time.Millisecond,
		ShortBreakDuration:     50 * time.Millisecond,
		LongBreakDuration:      150 * time.Millisecond,
		SessionsUntilLongBreak: 4,
	}
	liveTimer := pomodoro_utils.NewTimer(testConfig)
	
	fmt.Println("Starting 100ms work session...")
	endTimeCh, doneCh := liveTimer.StartSession()
	fmt.Printf("Session ends at: %s\n", endTimeCh.Format("15:04:05.000"))
	
	start := time.Now()
	<-doneCh
	elapsed := time.Since(start)
	
	fmt.Printf("✅ Session completed in %v\n", elapsed)
	fmt.Printf("Updated stats: %+v\n\n", liveTimer.GetStats())

	// Example 10: Complete workflow
	fmt.Println("Example 10: Complete Pomodoro Workflow")
	fmt.Println("--------------------------------------")
	fmt.Println("A typical workflow:")
	fmt.Println("1. Create timer with desired configuration")
	fmt.Println("2. Start work session (25 min)")
	fmt.Println("3. Take short break (5 min)")
	fmt.Println("4. Repeat steps 2-3 for 4 sessions")
	fmt.Println("5. Take long break (15 min)")
	fmt.Println("6. Track statistics and streaks")
	fmt.Println("7. Set daily goals and track progress")
	fmt.Println()
	fmt.Println("Tips:")
	fmt.Println("- Break the streak if you miss a session")
	fmt.Println("- Use productivity score for motivation")
	fmt.Println("- Adjust timing to your preference")
}

func generateProgressBar(percentage, width float64) string {
	filled := int(percentage / 100 * width)
	bar := ""
	for i := 0; i < int(width); i++ {
		if i < filled {
			bar += "█"
		} else {
			bar += "░"
		}
	}
	return bar
}