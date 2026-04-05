package main

import (
	"context"
	"fmt"
	"time"

	"github.com/ayukyo/alltoolkit/Go/rate_limiter"
)

func main() {
	fmt.Println("=== Rate Limiter Examples ===\n")

	// Example 1: Token Bucket - API Rate Limiting
	fmt.Println("1. Token Bucket Rate Limiter")
	fmt.Println("   Use case: API rate limiting with burst capability")
	tokenBucketExample()
	fmt.Println()

	// Example 2: Fixed Window - Simple Rate Limiting
	fmt.Println("2. Fixed Window Rate Limiter")
	fmt.Println("   Use case: Simple requests per minute limiting")
	fixedWindowExample()
	fmt.Println()

	// Example 3: Sliding Window - Smooth Rate Limiting
	fmt.Println("3. Sliding Window Rate Limiter")
	fmt.Println("   Use case: Smooth rate limiting without burst at window boundaries")
	slidingWindowExample()
	fmt.Println()

	// Example 4: Leaky Bucket - Traffic Shaping
	fmt.Println("4. Leaky Bucket Rate Limiter")
	fmt.Println("   Use case: Traffic shaping with constant output rate")
	leakyBucketExample()
	fmt.Println()

	// Example 5: Multi Limiter - Combined Limits
	fmt.Println("5. Multi Limiter (Combined Limits)")
	fmt.Println("   Use case: Apply multiple rate limits simultaneously")
	multiLimiterExample()
	fmt.Println()

	// Example 6: Per-Client Limiter - User-based Rate Limiting
	fmt.Println("6. Per-Client Rate Limiter")
	fmt.Println("   Use case: Rate limit per user/API key")
	perClientExample()
	fmt.Println()

	// Example 7: Wait with Timeout
	fmt.Println("7. Wait with Timeout")
	fmt.Println("   Use case: Block until rate limit allows or timeout")
	waitExample()
	fmt.Println()

	// Example 8: Statistics and Monitoring
	fmt.Println("8. Statistics and Monitoring")
	statsExample()
	fmt.Println()

	fmt.Println("=== All Examples Completed ===")
}

func tokenBucketExample() {
	// Create a token bucket with capacity 10 and refill rate 2 tokens/second
	limiter := rate_limiter.NewTokenBucket(10, 2)
	defer limiter.Stop()

	// Simulate burst of requests
	fmt.Println("   Sending burst of 15 requests...")
	allowed := 0
	rejected := 0
	for i := 0; i < 15; i++ {
		if limiter.Allow() {
			allowed++
		} else {
			rejected++
		}
	}
	fmt.Printf("   Allowed: %d, Rejected: %d\n", allowed, rejected)

	// Wait for tokens to refill
	fmt.Println("   Waiting 2 seconds for refill...")
	time.Sleep(2 * time.Second)

	// Try again
	newAllowed := 0
	for i := 0; i < 5; i++ {
		if limiter.Allow() {
			newAllowed++
		}
	}
	fmt.Printf("   After refill - Allowed: %d\n", newAllowed)
}

func fixedWindowExample() {
	// Create fixed window: 5 requests per 2 seconds
	limiter := rate_limiter.NewFixedWindow(5, 2*time.Second)

	// Send requests
	fmt.Println("   Sending 7 requests...")
	for i := 0; i < 7; i++ {
		if limiter.Allow() {
			fmt.Printf("   Request %d: ALLOWED\n", i+1)
		} else {
			fmt.Printf("   Request %d: REJECTED (rate limited)\n", i+1)
		}
	}

	// Wait for window to reset
	fmt.Println("   Waiting 2.1 seconds for window reset...")
	time.Sleep(2100 * time.Millisecond)

	// Try again
	fmt.Println("   Sending 2 more requests...")
	for i := 0; i < 2; i++ {
		if limiter.Allow() {
			fmt.Printf("   Request %d: ALLOWED\n", i+1)
		} else {
			fmt.Printf("   Request %d: REJECTED\n", i+1)
		}
	}
}

func slidingWindowExample() {
	// Create sliding window: 3 requests per 2 seconds
	limiter := rate_limiter.NewSlidingWindow(3, 2*time.Second)

	// Send requests with delays
	fmt.Println("   Sending 4 requests with 500ms delays...")
	for i := 0; i < 4; i++ {
		if limiter.Allow() {
			fmt.Printf("   Request %d: ALLOWED\n", i+1)
		} else {
			fmt.Printf("   Request %d: REJECTED\n", i+1)
		}
		if i < 3 {
			time.Sleep(500 * time.Millisecond)
		}
	}

	// Wait for oldest request to expire
	fmt.Println("   Waiting 1.6 seconds for oldest request to expire...")
	time.Sleep(1600 * time.Millisecond)

	// Try again
	fmt.Println("   Sending 1 more request...")
	if limiter.Allow() {
		fmt.Println("   Request: ALLOWED (oldest expired)")
	} else {
		fmt.Println("   Request: REJECTED")
	}
}

func leakyBucketExample() {
	// Create leaky bucket: leak rate 2/sec, capacity 5
	limiter := rate_limiter.NewLeakyBucket(2, 5)
	defer limiter.Stop()

	// Fill bucket with burst
	fmt.Println("   Filling bucket with 7 requests...")
	allowed := 0
	for i := 0; i < 7; i++ {
		if limiter.Allow() {
			allowed++
			fmt.Printf("   Request %d: ALLOWED (added to bucket)\n", i+1)
		} else {
			fmt.Printf("   Request %d: REJECTED (bucket full)\n", i+1)
		}
	}

	// Wait for bucket to leak
	fmt.Println("   Waiting 1 second for bucket to leak...")
	time.Sleep(1 * time.Second)

	// Try again
	fmt.Println("   Sending 2 more requests...")
	for i := 0; i < 2; i++ {
		if limiter.Allow() {
			fmt.Printf("   Request %d: ALLOWED (space available)\n", i+1)
		} else {
			fmt.Printf("   Request %d: REJECTED\n", i+1)
		}
	}
}

func multiLimiterExample() {
	// Create two limiters
	perSecond := rate_limiter.NewTokenBucket(5, 5)    // 5 req/sec burst
	perMinute := rate_limiter.NewFixedWindow(10, time.Minute) // 10 req/min
	defer perSecond.Stop()

	// Combine them
	limiter := rate_limiter.NewMultiLimiter(perSecond, perMinute)

	// Send requests
	fmt.Println("   Sending 12 requests (limited by both per-second and per-minute)...")
	for i := 0; i < 12; i++ {
		if limiter.Allow() {
			fmt.Printf("   Request %d: ALLOWED\n", i+1)
		} else {
			fmt.Printf("   Request %d: REJECTED\n", i+1)
		}
	}
}

func perClientExample() {
	// Create per-client limiter with fixed window factory
	limiter := rate_limiter.NewPerClientLimiter(func() rate_limiter.Limiter {
		return rate_limiter.NewFixedWindow(3, time.Second)
	})
	defer limiter.Stop()

	// Simulate requests from different clients
	clients := []string{"user1", "user2", "user1", "user3", "user1", "user1", "user2"}

	fmt.Println("   Simulating requests from multiple clients...")
	for _, client := range clients {
		if limiter.Allow(client) {
			fmt.Printf("   Request from %s: ALLOWED\n", client)
		} else {
			fmt.Printf("   Request from %s: REJECTED (rate limited)\n", client)
		}
	}

	fmt.Printf("   Total unique clients: %d\n", limiter.ClientCount())
}

func waitExample() {
	// Create token bucket with 1 capacity
	limiter := rate_limiter.NewTokenBucket(1, 0.5) // 0.5 tokens/sec
	defer limiter.Stop()

	// Use the token
	limiter.Allow()
	fmt.Println("   Token used, bucket empty")

	// Try to wait for token with timeout
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	fmt.Println("   Waiting for token (max 3 seconds)...")
	start := time.Now()
	err := limiter.Wait(ctx)
	elapsed := time.Since(start)

	if err != nil {
		fmt.Printf("   Wait failed: %v\n", err)
	} else {
		fmt.Printf("   Token acquired after %v\n", elapsed.Round(time.Millisecond))
	}

	// Try with short timeout (should fail)
	limiter.Allow() // Use token again
	ctx2, cancel2 := context.WithTimeout(context.Background(), 500*time.Millisecond)
	defer cancel2()

	fmt.Println("   Waiting with 500ms timeout...")
	err = limiter.Wait(ctx2)
	if err != nil {
		fmt.Printf("   Wait failed as expected: %v\n", err)
	}
}

func statsExample() {
	// Create limiter
	limiter := rate_limiter.NewTokenBucket(10, 1)
	defer limiter.Stop()

	// Simulate some traffic
	fmt.Println("   Simulating traffic...")
	for i := 0; i < 15; i++ {
		limiter.Allow()
	}

	// Get stats
	stats := limiter.Stats()
	fmt.Printf("   Statistics:\n")
	fmt.Printf("     Capacity:  %d\n", stats.Capacity)
	fmt.Printf("     Remaining: %d\n", stats.Remaining)
	fmt.Printf("     Allowed:   %d\n", stats.Allowed)
	fmt.Printf("     Rejected:  %d\n", stats.Rejected)

	// Reset and show new stats
	limiter.Reset()
	stats = limiter.Stats()
	fmt.Printf("   After reset:\n")
	fmt.Printf("     Remaining: %d\n", stats.Remaining)
	fmt.Printf("     Allowed:   %d\n", stats.Allowed)
}