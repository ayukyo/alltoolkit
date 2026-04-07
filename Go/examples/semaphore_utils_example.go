// Example: Semaphore Utilities
//
// This example demonstrates various use cases for the semaphore_utils package,
// including rate limiting, connection pooling, resource management, and
// weighted semaphores for variable resource allocation.
//
// Run: go run semaphore_utils_example.go
package main

import (
	"context"
	"fmt"
	"log"
	"sync"
	"time"

	"github.com/ayukyo/alltoolkit/Go/semaphore_utils"
)

func main() {
	fmt.Println("=== Semaphore Utilities Examples ===\n")

	// Example 1: Basic semaphore for rate limiting
	exampleBasicRateLimit()

	// Example 2: Weighted semaphore for resource management
	exampleWeightedResource()

	// Example 3: Semaphore pool for multi-resource management
	exampleSemaphorePool()

	// Example 4: Timeout handling
	exampleTimeout()

	// Example 5: Context cancellation
	exampleContextCancellation()

	// Example 6: Non-blocking operations
	exampleNonBlocking()

	// Example 7: Using helper functions
	exampleHelperFunctions()

	// Example 8: Batch operations
	exampleBatchOperations()

	// Example 9: Concurrent worker pool
	exampleWorkerPool()

	// Example 10: Priority-based resource allocation
	examplePriorityAllocation()

	fmt.Println("\n=== All examples completed ===")
}

// Example 1: Basic rate limiting with semaphore
func exampleBasicRateLimit() {
	fmt.Println("--- Example 1: Basic Rate Limiting ---")

	// Create semaphore allowing 3 concurrent operations
	sem := semaphore_utils.New(3)
	ctx := context.Background()

	var wg sync.WaitGroup

	// Launch 10 goroutines
	for i := 1; i <= 10; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()

			// Acquire permit
			if err := sem.Acquire(ctx); err != nil {
				log.Printf("Worker %d: Failed to acquire: %v", id, err)
				return
			}
			defer sem.Release()

			fmt.Printf("Worker %d: Processing (available: %d)\n", id, sem.Available())
			time.Sleep(500 * time.Millisecond) // Simulate work
			fmt.Printf("Worker %d: Done\n", id)
		}(i)
	}

	wg.Wait()
	fmt.Println()
}

// Example 2: Weighted semaphore for variable resource usage
func exampleWeightedResource() {
	fmt.Println("--- Example 2: Weighted Resource Management ---")

	// Create weighted semaphore with total capacity of 10 units
	sem := semaphore_utils.NewWeighted(10)
	ctx := context.Background()

	// Different tasks require different amounts of resources
	tasks := []struct {
		name   string
		weight int64
	}{
		{"Small Task", 2},
		{"Medium Task", 4},
		{"Large Task", 6},
		{"Small Task 2", 2},
	}

	var wg sync.WaitGroup

	for _, task := range tasks {
		wg.Add(1)
		go func(name string, weight int64) {
			defer wg.Done()

			fmt.Printf("%s: Trying to acquire %d units (available: %d)\n",
				name, weight, sem.Available())

			if err := sem.Acquire(ctx, weight); err != nil {
				log.Printf("%s: Failed to acquire: %v", name, err)
				return
			}
			defer sem.Release(weight)

			fmt.Printf("%s: Acquired %d units (in use: %d)\n", name, weight, sem.InUse())
			time.Sleep(300 * time.Millisecond)
			fmt.Printf("%s: Completed\n", name)
		}(task.name, task.weight)
	}

	wg.Wait()
	fmt.Println()
}

// Example 3: Semaphore pool for managing different resources
func exampleSemaphorePool() {
	fmt.Println("--- Example 3: Semaphore Pool ---")

	// Create pool with default capacity of 2 per resource
	pool := semaphore_utils.NewPool(2)

	// Simulate different API endpoints with rate limits
	endpoints := []string{"api/users", "api/orders", "api/products", "api/users"}

	var wg sync.WaitGroup

	for _, endpoint := range endpoints {
		wg.Add(1)
		go func(ep string) {
			defer wg.Done()

			// Get semaphore for this endpoint
			sem := pool.Get(ep)
			ctx := context.Background()

			if err := sem.Acquire(ctx); err != nil {
				log.Printf("Failed to acquire for %s: %v", ep, err)
				return
			}
			defer sem.Release()

			fmt.Printf("Calling %s (pool size: %d)\n", ep, pool.Size())
			time.Sleep(200 * time.Millisecond)
			fmt.Printf("Completed %s\n", ep)
		}(endpoint)
	}

	wg.Wait()

	fmt.Printf("Final pool keys: %v\n", pool.Keys())
	fmt.Println()
}

// Example 4: Timeout handling
func exampleTimeout() {
	fmt.Println("--- Example 4: Timeout Handling ---")

	sem := semaphore_utils.New(1)
	ctx := context.Background()

	// Acquire the only permit
	sem.Acquire(ctx)
	fmt.Println("Acquired permit, simulating long operation...")

	// Try to acquire with timeout in another goroutine
	go func() {
		fmt.Println("Trying to acquire with 500ms timeout...")
		err := sem.AcquireTimeout(500 * time.Millisecond)
		if err == semaphore_utils.ErrTimeout {
			fmt.Println("Timeout! Could not acquire permit in time.")
		} else if err != nil {
			log.Printf("Error: %v", err)
		} else {
			defer sem.Release()
			fmt.Println("Acquired after waiting")
		}
	}()

	time.Sleep(1 * time.Second)
	fmt.Println("Releasing permit...")
	sem.Release()

	time.Sleep(100 * time.Millisecond)
	fmt.Println()
}

// Example 5: Context cancellation
func exampleContextCancellation() {
	fmt.Println("--- Example 5: Context Cancellation ---")

	sem := semaphore_utils.New(1)
	ctx, cancel := context.WithCancel(context.Background())

	// Acquire the only permit
	sem.Acquire(ctx)
	fmt.Println("Acquired permit, will cancel context...")

	// Start waiting goroutine
	done := make(chan bool)
	go func() {
		fmt.Println("Goroutine: Waiting for permit...")
		err := sem.Acquire(ctx)
		if err == semaphore_utils.ErrCancelled {
			fmt.Println("Goroutine: Cancelled while waiting")
		} else if err != nil {
			log.Printf("Goroutine: Error: %v", err)
		} else {
			defer sem.Release()
			fmt.Println("Goroutine: Acquired permit")
		}
		done <- true
	}()

	time.Sleep(300 * time.Millisecond)
	fmt.Println("Cancelling context...")
	cancel()

	<-done
	time.Sleep(100 * time.Millisecond)
	sem.Release() // Release the original permit
	fmt.Println()
}

// Example 6: Non-blocking operations
func exampleNonBlocking() {
	fmt.Println("--- Example 6: Non-blocking Operations ---")

	sem := semaphore_utils.New(2)
	ctx := context.Background()

	// Acquire both permits
	sem.Acquire(ctx)
	sem.Acquire(ctx)
	fmt.Println("Acquired both permits")

	// Try non-blocking acquire
	if sem.TryAcquire() {
		fmt.Println("Unexpected: Got permit (should be full)")
		sem.Release()
	} else {
		fmt.Println("TryAcquire failed as expected (semaphore full)")
	}

	// Release one and try again
	sem.Release()
	fmt.Println("Released one permit")

	if sem.TryAcquire() {
		fmt.Println("TryAcquire succeeded after release")
		sem.Release()
	} else {
		fmt.Println("Unexpected: TryAcquire failed")
	}

	sem.Release()
	fmt.Println()
}

// Example 7: Helper functions
func exampleHelperFunctions() {
	fmt.Println("--- Example 7: Helper Functions ---")

	sem := semaphore_utils.New(2)
	ctx := context.Background()

	// RunWithSemaphore
	err := semaphore_utils.RunWithSemaphore(ctx, sem, func() error {
		fmt.Println("Running with semaphore (automatic acquire/release)")
		time.Sleep(200 * time.Millisecond)
		return nil
	})
	if err != nil {
		log.Printf("Error: %v", err)
	}

	// RunWithTimeout
	err = semaphore_utils.RunWithTimeout(1*time.Second, sem, func() error {
		fmt.Println("Running with timeout")
		time.Sleep(100 * time.Millisecond)
		return nil
	})
	if err != nil {
		log.Printf("Error: %v", err)
	}

	// RunWeightedWithSemaphore
	weightedSem := semaphore_utils.NewWeighted(10)
	err = semaphore_utils.RunWeightedWithSemaphore(ctx, weightedSem, 5, func() error {
		fmt.Println("Running with weighted semaphore (5 units)")
		time.Sleep(100 * time.Millisecond)
		return nil
	})
	if err != nil {
		log.Printf("Error: %v", err)
	}

	fmt.Println()
}

// Example 8: Batch operations
func exampleBatchOperations() {
	fmt.Println("--- Example 8: Batch Operations ---")

	sem1 := semaphore_utils.NewWeighted(10)
	sem2 := semaphore_utils.NewWeighted(10)
	ctx := context.Background()

	// Acquire some units first
	sem1.Acquire(ctx, 3)
	sem2.Acquire(ctx, 2)

	fmt.Printf("Before batch: sem1=%d, sem2=%d\n", sem1.InUse(), sem2.InUse())

	// Batch acquire from multiple semaphores
	release, err := semaphore_utils.BatchAcquire(ctx, map[*semaphore_utils.WeightedSemaphore]int64{
		sem1: 4,
		sem2: 5,
	})

	if err != nil {
		log.Printf("Batch acquire failed: %v", err)
		return
	}

	fmt.Printf("After batch acquire: sem1=%d, sem2=%d\n", sem1.InUse(), sem2.InUse())

	// Do work...
	time.Sleep(200 * time.Millisecond)

	// Release all at once
	release()
	fmt.Printf("After batch release: sem1=%d, sem2=%d\n", sem1.InUse(), sem2.InUse())

	// Clean up
	sem1.Release(3)
	sem2.Release(2)

	fmt.Println()
}

// Example 9: Concurrent worker pool
func exampleWorkerPool() {
	fmt.Println("--- Example 9: Concurrent Worker Pool ---")

	const numWorkers = 3
	const numTasks = 10

	sem := semaphore_utils.New(numWorkers)
	ctx := context.Background()

	taskQueue := make(chan int, numTasks)
	results := make(chan int, numTasks)

	// Start workers
	var wg sync.WaitGroup
	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			for taskID := range taskQueue {
				if err := sem.Acquire(ctx); err != nil {
					log.Printf("Worker %d: Failed to acquire: %v", workerID, err)
					continue
				}
				defer sem.Release()

				fmt.Printf("Worker %d: Processing task %d\n", workerID, taskID)
				time.Sleep(100 * time.Millisecond) // Simulate work
				results <- taskID * 2
			}
		}(i)
	}

	// Queue tasks
	for i := 0; i < numTasks; i++ {
		taskQueue <- i
	}
	close(taskQueue)

	// Collect results
	go func() {
		wg.Wait()
		close(results)
	}()

	count := 0
	for result := range results {
		count++
		_ = result
	}

	fmt.Printf("Processed %d tasks\n", count)
	fmt.Println()
}

// Example 10: Priority-based allocation with weighted semaphore
func examplePriorityAllocation() {
	fmt.Println("--- Example 10: Priority-based Allocation ---")

	// Simulate a system with 100 resource units
	sem := semaphore_utils.NewWeighted(100)
	ctx := context.Background()

	// High priority task: needs 60 units
	// Medium priority task: needs 30 units
	// Low priority task: needs 20 units

	tasks := []struct {
		name     string
		priority string
		weight   int64
	}{
		{"Low Priority", "low", 20},
		{"High Priority", "high", 60},
		{"Medium Priority", "medium", 30},
	}

	var wg sync.WaitGroup

	for _, task := range tasks {
		wg.Add(1)
		go func(name, priority string, weight int64) {
			defer wg.Done()

			// In real scenario, you might implement actual priority queuing
			// Here we just demonstrate the weighted allocation

			start := time.Now()
			if err := sem.Acquire(ctx, weight); err != nil {
				log.Printf("%s: Failed: %v", name, err)
				return
			}
			elapsed := time.Since(start)

			fmt.Printf("[%s] %s: Acquired %d units (waited %v)\n",
				priority, name, weight, elapsed)

			time.Sleep(200 * time.Millisecond)
			sem.Release(weight)
			fmt.Printf("[%s] %s: Completed\n", priority, name)
		}(task.name, task.priority, task.weight)
	}

	wg.Wait()
	fmt.Println()
}