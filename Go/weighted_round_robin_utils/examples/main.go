// Example usage of weighted round-robin load balancing algorithms.
package main

import (
	"fmt"
	"sync/atomic"
	"time"

	weightedroundrobin "github.com/ayukyo/alltoolkit/Go/weighted_round_robin_utils"
)

func main() {
	fmt.Println("=== Weighted Round-Robin Load Balancing Examples ===")
	fmt.Println()

	// Example 1: Basic Weighted Round-Robin
	fmt.Println("--- Example 1: Weighted Round-Robin ---")
	basicWeightedRoundRobin()

	// Example 2: Smooth Weighted Round-Robin (Nginx-style)
	fmt.Println()
	fmt.Println("--- Example 2: Smooth Weighted Round-Robin ---")
	smoothWeightedRoundRobin()

	// Example 3: Weighted Random Selection
	fmt.Println()
	fmt.Println("--- Example 3: Weighted Random Selection ---")
	weightedRandom()

	// Example 4: Least Connections
	fmt.Println()
	fmt.Println("--- Example 4: Least Connections ---")
	leastConnections()

	// Example 5: Weighted Least Connections
	fmt.Println()
	fmt.Println("--- Example 5: Weighted Least Connections ---")
	weightedLeastConnections()

	// Example 6: Power of Two Choices
	fmt.Println()
	fmt.Println("--- Example 6: Power of Two Choices ---")
	powerOfTwoChoices()

	// Example 7: Simulated Load Balancer
	fmt.Println()
	fmt.Println("--- Example 7: Simulated Load Balancer ---")
	simulatedLoadBalancer()
}

func basicWeightedRoundRobin() {
	// Create backends with different weights
	backends := []*weightedroundrobin.Backend{
		weightedroundrobin.NewBackend("server-a", 5), // 50% traffic
		weightedroundrobin.NewBackend("server-b", 3), // 30% traffic
		weightedroundrobin.NewBackend("server-c", 2), // 20% traffic
	}

	wrr, err := weightedroundrobin.NewWeightedRoundRobin(backends)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	// Simulate 10 requests
	fmt.Println("Selecting backends for 10 requests:")
	counts := make(map[string]int)
	for i := 0; i < 10; i++ {
		selected := wrr.Select()
		counts[selected.Name]++
		fmt.Printf("  Request %d -> %s\n", i+1, selected.Name)
	}

	fmt.Println("\nDistribution:")
	for name, count := range counts {
		fmt.Printf("  %s: %d selections\n", name, count)
	}
}

func smoothWeightedRoundRobin() {
	// Nginx-style smooth weighted round-robin
	// Provides better distribution, avoiding "thundering herd" problems
	backends := []*weightedroundrobin.Backend{
		weightedroundrobin.NewBackend("heavy", 5),
		weightedroundrobin.NewBackend("medium", 2),
		weightedroundrobin.NewBackend("light", 1),
	}

	swrr, err := weightedroundrobin.NewSmoothWeightedRoundRobin(backends)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	// One complete cycle (sum of weights = 8)
	fmt.Println("One complete cycle (smooth distribution):")
	sequence := make([]string, 0, 8)
	for i := 0; i < 8; i++ {
		selected := swrr.Select()
		sequence = append(sequence, selected.Name)
	}

	for i, name := range sequence {
		fmt.Printf("  %d: %s\n", i+1, name)
	}

	fmt.Println("\nSmooth distribution pattern: [heavy, heavy, heavy, medium, heavy, medium, heavy, light]")
	fmt.Println("This avoids consecutive heavy server selections")
}

func weightedRandom() {
	// Probability-based selection
	backends := []*weightedroundrobin.Backend{
		weightedroundrobin.NewBackend("primary", 70),   // 70% chance
		weightedroundrobin.NewBackend("secondary", 20), // 20% chance
		weightedroundrobin.NewBackend("fallback", 10),  // 10% chance
	}

	wr, err := weightedroundrobin.NewWeightedRandom(backends)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	// Simulate 100 selections
	counts := make(map[string]int)
	for i := 0; i < 100; i++ {
		selected := wr.Select()
		counts[selected.Name]++
	}

	fmt.Println("Random distribution over 100 selections:")
	for name, count := range counts {
		percentage := float64(count) / 100.0 * 100.0
		fmt.Printf("  %s: %d (%.1f%%)\n", name, count, percentage)
	}
}

func leastConnections() {
	// Select backend with fewest active connections
	backends := []*weightedroundrobin.Backend{
		weightedroundrobin.NewBackend("server-1", 1),
		weightedroundrobin.NewBackend("server-2", 1),
		weightedroundrobin.NewBackend("server-3", 1),
	}

	lc, err := weightedroundrobin.NewLeastConnections(backends)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	// Simulate some connections
	backends[0].Incr()
	backends[0].Incr()
	backends[0].Incr() // server-1: 3 connections
	backends[1].Incr() // server-2: 1 connection
	// server-3: 0 connections

	fmt.Println("Current connection counts:")
	for _, b := range backends {
		fmt.Printf("  %s: %d connections\n", b.Name, b.GetConnections())
	}

	// Select backend with least connections
	selected := lc.Select()
	fmt.Printf("\nSelected: %s (has fewest connections)\n", selected.Name)
}

func weightedLeastConnections() {
	// Combine weight and connection count for optimal load distribution
	backends := []*weightedroundrobin.Backend{
		weightedroundrobin.NewBackend("high-capacity", 10),  // Can handle more load
		weightedroundrobin.NewBackend("medium-capacity", 5),
		weightedroundrobin.NewBackend("low-capacity", 2),
	}

	wlc, err := weightedroundrobin.NewWeightedLeastConnections(backends)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	// Simulate connections
	// high-capacity: 20 connections / 10 weight = 2.0 ratio
	// medium-capacity: 5 connections / 5 weight = 1.0 ratio
	// low-capacity: 1 connection / 2 weight = 0.5 ratio (best choice!)
	backends[0].Incr()
	for i := 0; i < 20; i++ {
		backends[0].Incr()
		backends[0].Decr()
	}
	backends[0].Incr() // Now 20 connections

	for i := 0; i < 5; i++ {
		backends[1].Incr() // 5 connections
	}

	backends[2].Incr() // 1 connection

	fmt.Println("Connection to weight ratios:")
	for _, b := range backends {
		ratio := float64(b.GetConnections()) / float64(b.Weight)
		fmt.Printf("  %s: %d conn / %d weight = %.2f ratio\n",
			b.Name, b.GetConnections(), b.Weight, ratio)
	}

	selected := wlc.Select()
	fmt.Printf("\nSelected: %s (lowest ratio)\n", selected.Name)
}

func powerOfTwoChoices() {
	// O(1) complexity with good load distribution
	// Pick 2 random backends, select the one with fewer connections
	backends := []*weightedroundrobin.Backend{
		weightedroundrobin.NewBackend("node-1", 1),
		weightedroundrobin.NewBackend("node-2", 1),
		weightedroundrobin.NewBackend("node-3", 1),
		weightedroundrobin.NewBackend("node-4", 1),
	}

	p2c, err := weightedroundrobin.NewPowerOfTwoChoices(backends)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	// Add some connections
	for i := 0; i < 10; i++ {
		backends[0].Incr()
	}

	fmt.Println("Connection counts:")
	for _, b := range backends {
		fmt.Printf("  %s: %d\n", b.Name, b.GetConnections())
	}

	// With node-1 having 10 connections, it should rarely be selected
	counts := make(map[string]int)
	for i := 0; i < 100; i++ {
		selected := p2c.Select()
		counts[selected.Name]++
	}

	fmt.Println("\nSelection distribution over 100 requests:")
	for name, count := range counts {
		fmt.Printf("  %s: %d\n", name, count)
	}
}

func simulatedLoadBalancer() {
	// Simulate a real load balancer scenario
	backends := []*weightedroundrobin.Backend{
		weightedroundrobin.NewBackend("backend-alpha", 4),
		weightedroundrobin.NewBackend("backend-beta", 2),
		weightedroundrobin.NewBackend("backend-gamma", 1),
	}

	// Use Smooth Weighted Round-Robin for production-like behavior
	lb, err := weightedroundrobin.NewSmoothWeightedRoundRobin(backends)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	fmt.Println("Simulating load balancer with 50 concurrent requests...")
	fmt.Println("Backends:")
	for _, b := range backends {
		fmt.Printf("  %s (weight: %d)\n", b.Name, b.Weight)
	}

	// Process requests
	for i := 0; i < 50; i++ {
		backend := lb.Select()
		
		// Simulate connection handling
		backend.Incr()
		
		// Simulate some work
		go func(b *weightedroundrobin.Backend, reqNum int) {
			time.Sleep(time.Millisecond * 10)
			b.Decr()
		}(backend, i)
	}

	// Let some requests complete
	time.Sleep(time.Millisecond * 50)

	// Show current state
	fmt.Println("\nCurrent backend states:")
	for _, b := range backends {
		active := atomic.LoadInt64(&b.Connections)
		fmt.Printf("  %s: %d active connections\n", b.Name, active)
	}

	// Continue processing
	fmt.Println("\nProcessing remaining requests...")
	for i := 0; i < 20; i++ {
		backend := lb.Select()
		fmt.Printf("  Request %d -> %s\n", i+1, backend.Name)
	}
}