// Package main demonstrates usage of scheduler_utils
package main

import (
	"context"
	"fmt"
	"time"

	scheduler "github.com/ayukyo/alltoolkit/Go/scheduler_utils"
)

func main() {
	fmt.Println("=== Scheduler Utils Demo ===")
	fmt.Println()

	// Demo 1: Basic Scheduler
	fmt.Println("--- Demo 1: Basic Scheduler ---")
	demoBasicScheduler()

	// Demo 2: One-time Tasks
	fmt.Println("\n--- Demo 2: One-time Tasks ---")
	demoOnceTasks()

	// Demo 3: Interval Tasks
	fmt.Println("\n--- Demo 3: Interval Tasks ---")
	demoIntervalTasks()

	// Demo 4: Task with Options
	fmt.Println("\n--- Demo 4: Task with Options ---")
	demoTaskWithOptions()

	// Demo 5: Task Management
	fmt.Println("\n--- Demo 5: Task Management ---")
	demoTaskManagement()

	// Demo 6: Delay Queue
	fmt.Println("\n--- Demo 6: Delay Queue ---")
	demoDelayQueue()

	// Demo 7: Rate Limiting
	fmt.Println("\n--- Demo 7: Rate Limiting ---")
	demoRateLimiting()

	fmt.Println("\n=== All Demos Complete ===")
}

func demoBasicScheduler() {
	// Create a new scheduler
	s := scheduler.NewScheduler()
	s.Start()
	defer s.Stop()

	// Schedule a simple task
	task, err := s.ScheduleOnce("hello", func(ctx context.Context) error {
		fmt.Println("  Hello from scheduled task!")
		return nil
	}, time.Now().Add(100*time.Millisecond))

	if err != nil {
		fmt.Printf("  Error: %v\n", err)
		return
	}

	fmt.Printf("  Task created: %s\n", task.TaskInfo())
	time.Sleep(200 * time.Millisecond)
	fmt.Printf("  Task status after execution: %s\n", task.Status)
}

func demoOnceTasks() {
	s := scheduler.NewScheduler()
	s.Start()
	defer s.Stop()

	// Schedule at specific time
	task1, _ := s.ScheduleOnce("specific-time",
		func(ctx context.Context) error {
			fmt.Println("  Task executed at specific time")
			return nil
		},
		time.Now().Add(50*time.Millisecond),
	)

	// Schedule after a duration
	task2, _ := s.ScheduleAfter("after-duration",
		func(ctx context.Context) error {
			fmt.Println("  Task executed after duration")
			return nil
		},
		100*time.Millisecond,
	)

	fmt.Printf("  Created tasks: %s, %s\n", task1.ID, task2.ID)
	time.Sleep(200 * time.Millisecond)
}

func demoIntervalTasks() {
	s := scheduler.NewScheduler()
	s.Start()
	defer s.Stop()

	count := 0
	task, _ := s.ScheduleTask("counter",
		func(ctx context.Context) error {
			count++
			fmt.Printf("  Interval tick #%d\n", count)
			return nil
		},
		scheduler.Every(100*time.Millisecond).WithMaxRuns(3), // Stop after 3 runs
	)

	fmt.Printf("  Interval task created: %s\n", task.ID)
	time.Sleep(400 * time.Millisecond)
	fmt.Printf("  Final count: %d\n", count)
}

func demoTaskWithOptions() {
	s := scheduler.NewScheduler()
	s.Start()
	defer s.Stop()

	task, _ := s.ScheduleOnce("important-task",
		func(ctx context.Context) error {
			fmt.Println("  Important task executed!")
			return nil
		},
		time.Now().Add(50*time.Millisecond),
		scheduler.WithPriority(10),
		scheduler.WithTags("production", "critical"),
		scheduler.WithDescription("This is a critical production task"),
	)

	fmt.Printf("  Task: %s\n", task.TaskInfo())
	fmt.Printf("  Description: %s\n", task.Description)

	// Find by tag
	tasks := s.ListTasksByTag("production")
	fmt.Printf("  Tasks with 'production' tag: %d\n", len(tasks))

	time.Sleep(100 * time.Millisecond)
}

func demoTaskManagement() {
	s := scheduler.NewScheduler()
	s.Start()
	defer s.Stop()

	// Create multiple tasks
	task1, _ := s.ScheduleOnce("task-1", func(ctx context.Context) error {
		return nil
	}, time.Now().Add(1*time.Hour))

	task2, _ := s.ScheduleOnce("task-2", func(ctx context.Context) error {
		return nil
	}, time.Now().Add(1*time.Hour))

	task3, _ := s.ScheduleOnce("task-3", func(ctx context.Context) error {
		return nil
	}, time.Now().Add(1*time.Hour))

	fmt.Printf("  Created 3 tasks, total: %d\n", s.TaskCount())

	// List all tasks
	tasks := s.ListTasks()
	fmt.Printf("  Listed tasks: %d\n", len(tasks))

	// Cancel one task
	s.Cancel(task2.ID)
	fmt.Printf("  After cancel, total: %d\n", s.TaskCount())

	// Get specific task
	if t, err := s.GetTask(task1.ID); err == nil {
		fmt.Printf("  Found task: %s\n", t.Name)
	}

	// task3 is also pending, but we're showing cancellation on task2
	_ = task3

	// Clear all
	s.Clear()
	fmt.Printf("  After clear, total: %d\n", s.TaskCount())
}

func demoDelayQueue() {
	dq := scheduler.NewDelayQueue()
	defer dq.Close()

	fmt.Println("  Scheduling delayed tasks...")

	// Schedule in reverse order - they'll execute in correct order
	dq.Schedule(300*time.Millisecond, func() {
		fmt.Println("  Third (300ms)")
	})

	dq.Schedule(100*time.Millisecond, func() {
		fmt.Println("  First (100ms)")
	})

	dq.Schedule(200*time.Millisecond, func() {
		fmt.Println("  Second (200ms)")
	})

	fmt.Println("  Waiting for execution...")
	time.Sleep(400 * time.Millisecond)
}

func demoRateLimiting() {
	s := scheduler.NewScheduler()
	s.Start()
	defer s.Stop()

	// Rate limiter: 2 tokens, refill 1 per second
	rls := scheduler.NewRateLimitScheduler(s, 2, 1)

	start := time.Now()
	executed := 0

	// Schedule 4 tasks to run immediately
	for i := 0; i < 4; i++ {
		taskNum := i + 1
		_, _ = rls.ScheduleOnce(fmt.Sprintf("rate-limited-%d", taskNum),
			func(ctx context.Context) error {
				elapsed := time.Since(start).Milliseconds()
				fmt.Printf("  Task %d executed at %dms\n", taskNum, elapsed)
				executed++
				return nil
			},
			time.Now(),
		)
	}

	// First 2 execute immediately, others wait for tokens
	time.Sleep(500 * time.Millisecond)
	fmt.Printf("  Total executed: %d\n", executed)
}