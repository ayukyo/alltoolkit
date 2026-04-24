// Example usage of debounce_utils package
package main

import (
	"context"
	"fmt"
	"time"

	debounce "github.com/ayukyo/alltoolkit/Go/debounce_utils"
)

func main() {
	fmt.Println("=== Debounce Utils Examples ===\n")

	// 1. Basic Debounce
	exampleBasicDebounce()

	// 2. Debounce with Leading Edge
	exampleLeadingDebounce()

	// 3. Debounce with MaxWait
	exampleMaxWaitDebounce()

	// 4. Throttler Basic
	exampleBasicThrottler()

	// 5. Rate Limiter
	exampleRateLimiter()

	// 6. Batch Processing
	exampleBatch()

	// 7. Delay
	exampleDelay()

	// 8. Real-world: Search Input Debounce
	exampleSearchDebounce()

	// 9. Real-world: API Rate Limiting
	exampleAPIRateLimiting()

	// 10. Real-world: Log Batching
	exampleLogBatching()
}

func exampleBasicDebounce() {
	fmt.Println("--- Basic Debounce ---")
	fmt.Println("Multiple rapid calls, only last one executes after delay")

	d := debounce.NewDebouncer(100 * time.Millisecond)
	defer d.Close()

	results := make(chan string, 5)

	// Simulate rapid input
	for i := 1; i <= 3; i++ {
		val := i
		d.Call(func() {
			results <- fmt.Sprintf("Call %d", val)
		})
		time.Sleep(20 * time.Millisecond)
	}

	// Wait for debounce
	time.Sleep(150 * time.Millisecond)

	select {
	case result := <-results:
		fmt.Printf("Executed: %s\n", result)
	default:
		fmt.Println("No execution")
	}
	fmt.Println()
}

func exampleLeadingDebounce() {
	fmt.Println("--- Leading Edge Debounce ---")
	fmt.Println("First call executes immediately, subsequent calls debounced")

	d := debounce.NewDebouncer(100*time.Millisecond, debounce.WithLeading())
	defer d.Close()

	var executed []string

	// First call executes immediately
	d.Call(func() { executed = append(executed, "First") })
	time.Sleep(10 * time.Millisecond)

	// These are debounced
	d.Call(func() { executed = append(executed, "Second") })
	d.Call(func() { executed = append(executed, "Third") })

	time.Sleep(150 * time.Millisecond)

	fmt.Printf("Executed: %v\n", executed)
	fmt.Println()
}

func exampleMaxWaitDebounce() {
	fmt.Println("--- Debounce with MaxWait ---")
	fmt.Println("Function executes after maxWait even with continuous calls")

	d := debounce.NewDebouncer(
		100*time.Millisecond,
		debounce.WithMaxWait(50*time.Millisecond),
	)
	defer d.Close()

	executed := false

	// Keep calling rapidly
	for i := 0; i < 10; i++ {
		d.Call(func() { executed = true })
		time.Sleep(10 * time.Millisecond)
	}

	// MaxWait should have triggered execution
	fmt.Printf("Executed: %v\n", executed)
	fmt.Println()
}

func exampleBasicThrottler() {
	fmt.Println("--- Basic Throttler ---")
	fmt.Println("Function executes at most once per interval")

	th := debounce.NewThrottler(100 * time.Millisecond)
	defer th.Close()

	var count int

	// Rapid calls
	for i := 0; i < 5; i++ {
		th.Call(func() { count++ })
		time.Sleep(30 * time.Millisecond)
	}

	time.Sleep(150 * time.Millisecond)
	fmt.Printf("Total executions: %d (out of 5 calls)\n", count)
	fmt.Println()
}

func exampleRateLimiter() {
	fmt.Println("--- Rate Limiter ---")
	fmt.Println("Token bucket rate limiting (10 req/sec, burst 3)")

	rl := debounce.NewRateLimiter(10, 3)

	for i := 1; i <= 5; i++ {
		if rl.Allow() {
			fmt.Printf("Request %d: Allowed (tokens: %.1f)\n", i, rl.Tokens())
		} else {
			fmt.Printf("Request %d: Rate limited\n", i)
		}
	}
	fmt.Println()
}

func exampleBatch() {
	fmt.Println("--- Batch Processing ---")
	fmt.Println("Items collected and processed in batches of 3")

	var batches [][]string

	b := debounce.NewBatch[string](3, debounce.WithBatchProcessor[string](func(items []string) {
		batches = append(batches, items)
		fmt.Printf("Processing batch: %v\n", items)
	}))

	b.Add("apple")
	b.Add("banana")
	b.Add("cherry") // Triggers batch
	b.Add("date")
	b.Add("elderberry")

	time.Sleep(50 * time.Millisecond)
	b.Flush() // Process remaining

	fmt.Printf("Total batches: %d\n", len(batches))
	fmt.Println()
}

func exampleDelay() {
	fmt.Println("--- Delay ---")
	fmt.Println("Enforce minimum time between function calls")

	d := debounce.NewDelay(50 * time.Millisecond)

	fmt.Println("Calling functions...")
	start := time.Now()

	d.Call(func() { fmt.Printf("First call (%.0fms)\n", float64(time.Since(start).Milliseconds())) })
	d.Call(func() { fmt.Printf("Second call (%.0fms)\n", float64(time.Since(start).Milliseconds())) })
	d.Call(func() { fmt.Printf("Third call (%.0fms)\n", float64(time.Since(start).Milliseconds())) })

	fmt.Println()
}

// Real-world examples

func exampleSearchDebounce() {
	fmt.Println("--- Real-world: Search Input Debounce ---")
	fmt.Println("Debouncing search API calls (wait for user to stop typing)")

	d := debounce.NewDebouncer(300 * time.Millisecond)
	defer d.Close()

	searchQueries := []string{"a", "ap", "app", "appl", "apple"}

	fmt.Println("User typing...")
	for i, query := range searchQueries {
		q := query
		fmt.Printf("  Typed: '%s'\n", q)
		d.Call(func() {
			fmt.Printf("  -> API call with query: '%s'\n", q)
		})
		time.Sleep(100 * time.Millisecond)
	}

	fmt.Println("User stopped typing...")
	time.Sleep(350 * time.Millisecond)
	fmt.Println()
}

func exampleAPIRateLimiting() {
	fmt.Println("--- Real-world: API Rate Limiting ---")
	fmt.Println("Rate limiting API calls (5 req/sec, burst 2)")

	rl := debounce.NewRateLimiter(5, 2)
	ctx := context.Background()

	fmt.Println("Making 6 API calls:")
	for i := 1; i <= 6; i++ {
		start := time.Now()
		err := rl.Wait(ctx)
		elapsed := time.Since(start)
		if err != nil {
			fmt.Printf("  Call %d: Error - %v\n", i, err)
		} else {
			fmt.Printf("  Call %d: Success (waited %.0fms)\n", i, float64(elapsed.Milliseconds()))
		}
	}
	fmt.Println()
}

func exampleLogBatching() {
	fmt.Println("--- Real-world: Log Batching ---")
	fmt.Println("Batching logs for efficient writing (batch size 5, timeout 100ms)")

	var totalLogs int

	b := debounce.NewBatch[string](5,
		debounce.WithBatchTimeout[string](100*time.Millisecond),
		debounce.WithBatchProcessor[string](func(logs []string) {
			totalLogs += len(logs)
			fmt.Printf("Writing %d logs to file: %v\n", len(logs), logs)
		}),
	)

	// Simulate log events
	for i := 1; i <= 8; i++ {
		b.Add(fmt.Sprintf("Log entry %d", i))
		time.Sleep(20 * time.Millisecond)
	}

	time.Sleep(150 * time.Millisecond)
	fmt.Printf("Total logs processed: %d\n", totalLogs)
	fmt.Println()
}