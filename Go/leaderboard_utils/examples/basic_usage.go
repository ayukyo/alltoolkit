package main

import (
	"fmt"
	"leaderboard_utils"
)

func main() {
	// Create a leaderboard (highest score first)
	lb := leaderboard_utils.NewLeaderboard(leaderboard_utils.LeaderboardConfig{})

	// Add players
	lb.AddOrUpdate("p1", "Alice", 1500)
	lb.AddOrUpdate("p2", "Bob", 2200)
	lb.AddOrUpdate("p3", "Charlie", 1800)
	lb.AddOrUpdate("p4", "Diana", 2500)
	lb.AddOrUpdate("p5", "Eve", 2000)

	fmt.Println("=== Basic Leaderboard Operations ===")
	fmt.Printf("Total entries: %d\n", lb.Count())

	// Get top 3
	top3 := lb.GetTopN(3)
	fmt.Println("\nTop 3 Players:")
	for _, entry := range top3 {
		fmt.Printf("  Rank %d: %s - Score: %.0f\n", entry.Rank, entry.Name, entry.Score)
	}

	// Get rank for a specific player
	rank, _ := lb.GetRank("p3")
	fmt.Printf("\nCharlie's rank: %d\n", rank)

	// Get percentile
	percentile, _ := lb.GetPercentile("p4")
	fmt.Printf("Diana's percentile: %.1f%% (top %.1f%%)\n", percentile, 100-percentile)

	// Get players around a rank (for "near me" views)
	aroundRank := lb.GetAroundRank(3, 1, 1)
	fmt.Println("\nPlayers around rank 3:")
	for _, entry := range aroundRank {
		fmt.Printf("  Rank %d: %s - Score: %.0f\n", entry.Rank, entry.Name, entry.Score)
	}

	// Update a player's score
	lb.AddOrUpdate("p2", "Bob", 2800)
	fmt.Println("\nAfter Bob's score update to 2800:")
	top3 = lb.GetTopN(3)
	for _, entry := range top3 {
		fmt.Printf("  Rank %d: %s - Score: %.0f\n", entry.Rank, entry.Name, entry.Score)
	}

	// Get statistics
	stats := lb.GetStats()
	fmt.Println("\n=== Leaderboard Statistics ===")
	fmt.Printf("Total Players: %d\n", stats.Count)
	fmt.Printf("Highest Score: %.0f\n", stats.MaxScore)
	fmt.Printf("Lowest Score: %.0f\n", stats.MinScore)
	fmt.Printf("Average Score: %.1f\n", stats.AvgScore)
	fmt.Printf("Median Score: %.0f\n", stats.MedianScore)

	// Ascending leaderboard (lowest score first)
	fmt.Println("\n=== Ascending Leaderboard ===")
	lbAsc := leaderboard_utils.NewLeaderboard(leaderboard_utils.LeaderboardConfig{Ascending: true})
	lbAsc.AddOrUpdate("p1", "Alice", 1500)
	lbAsc.AddOrUpdate("p2", "Bob", 2200)
	lbAsc.AddOrUpdate("p3", "Charlie", 1800)
	top3Asc := lbAsc.GetTopN(3)
	for _, entry := range top3Asc {
		fmt.Printf("  Rank %d: %s - Score: %.0f\n", entry.Rank, entry.Name, entry.Score)
	}

	// Max size leaderboard
	fmt.Println("\n=== Leaderboard with Max Size ===")
	lbLimited := leaderboard_utils.NewLeaderboard(leaderboard_utils.LeaderboardConfig{MaxSize: 3})
	lbLimited.AddOrUpdate("p1", "Alice", 1500)
	lbLimited.AddOrUpdate("p2", "Bob", 2200)
	lbLimited.AddOrUpdate("p3", "Charlie", 1800)
	lbLimited.AddOrUpdate("p4", "Diana", 2500)
	lbLimited.AddOrUpdate("p5", "Eve", 500) // Will evict lowest (Eve)
	fmt.Printf("Entries after adding with limit: %d\n", lbLimited.Count())
	fmt.Println("Top entries:")
	for _, entry := range lbLimited.GetTopN(3) {
		fmt.Printf("  Rank %d: %s - Score: %.0f\n", entry.Rank, entry.Name, entry.Score)
	}

	// Heap-based leaderboard for real-time updates
	fmt.Println("\n=== Heap-based Leaderboard ===")
	heap := leaderboard_utils.NewLeaderboardHeap(false)
	heap.Add(&leaderboard_utils.Entry{ID: "p1", Name: "Alice", Score: 1500})
	heap.Add(&leaderboard_utils.Entry{ID: "p2", Name: "Bob", Score: 2200})
	heap.Add(&leaderboard_utils.Entry{ID: "p3", Name: "Charlie", Score: 1800})
	fmt.Println("Sorted entries from heap:")
	for _, entry := range heap.GetSorted() {
		fmt.Printf("  Rank %d: %s - Score: %.0f\n", entry.Rank, entry.Name, entry.Score)
	}

	// Tie-breaking
	fmt.Println("\n=== Tie-Breaking Strategies ===")
	lbTie := leaderboard_utils.NewLeaderboard(leaderboard_utils.LeaderboardConfig{})
	lbTie.AddOrUpdate("p1", "Zoe", 1000)
	lbTie.AddOrUpdate("p2", "Alice", 1000)
	lbTie.AddOrUpdate("p3", "Bob", 1000)

	rankAlphabetical, _ := lbTie.GetRankWithTieBreak("p2", leaderboard_utils.TieBreakAlphabetical)
	fmt.Printf("Alice's rank (alphabetical tie-break): %d\n", rankAlphabetical)

	rankReverseAlphabetical, _ := lbTie.GetRankWithTieBreak("p1", leaderboard_utils.TieBreakReverseAlphabetical)
	fmt.Printf("Zoe's rank (reverse alphabetical tie-break): %d\n", rankReverseAlphabetical)

	// Merging leaderboards
	fmt.Println("\n=== Merging Leaderboards ===")
	lb1 := leaderboard_utils.NewLeaderboard(leaderboard_utils.LeaderboardConfig{})
	lb1.AddOrUpdate("p1", "Alice", 1000)
	lb1.AddOrUpdate("p2", "Bob", 1500)

	lb2 := leaderboard_utils.NewLeaderboard(leaderboard_utils.LeaderboardConfig{})
	lb2.AddOrUpdate("p2", "Bob", 2000) // Higher score
	lb2.AddOrUpdate("p3", "Charlie", 1800)

	lb1.Merge(lb2)
	fmt.Println("After merge:")
	for _, entry := range lb1.GetTopN(3) {
		fmt.Printf("  Rank %d: %s - Score: %.0f\n", entry.Rank, entry.Name, entry.Score)
	}
}