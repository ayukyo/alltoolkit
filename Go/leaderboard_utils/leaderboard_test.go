package leaderboard_utils

import (
	"math"
	"testing"
)

func TestNewLeaderboard(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{})
	if lb == nil {
		t.Fatal("Expected non-nil leaderboard")
	}
	if lb.Count() != 0 {
		t.Errorf("Expected empty leaderboard, got %d entries", lb.Count())
	}
}

func TestAddOrUpdate(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{})

	lb.AddOrUpdate("p1", "Player 1", 100)
	lb.AddOrUpdate("p2", "Player 2", 200)
	lb.AddOrUpdate("p3", "Player 3", 150)

	if lb.Count() != 3 {
		t.Errorf("Expected 3 entries, got %d", lb.Count())
	}

	// Update existing entry
	lb.AddOrUpdate("p1", "Player One", 300)

	if lb.Count() != 3 {
		t.Errorf("Expected 3 entries after update, got %d", lb.Count())
	}

	entry, exists := lb.GetEntry("p1")
	if !exists {
		t.Fatal("Expected to find p1")
	}
	if entry.Score != 300 {
		t.Errorf("Expected score 300, got %f", entry.Score)
	}
	if entry.Name != "Player One" {
		t.Errorf("Expected name 'Player One', got %s", entry.Name)
	}
}

func TestRemove(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{})
	lb.AddOrUpdate("p1", "Player 1", 100)

	removed := lb.Remove("p1")
	if !removed {
		t.Error("Expected successful removal")
	}
	if lb.Count() != 0 {
		t.Errorf("Expected empty leaderboard, got %d entries", lb.Count())
	}

	removed = lb.Remove("nonexistent")
	if removed {
		t.Error("Expected failed removal for nonexistent entry")
	}
}

func TestGetRank(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{})
	lb.AddOrUpdate("p1", "Player 1", 100)
	lb.AddOrUpdate("p2", "Player 2", 200)
	lb.AddOrUpdate("p3", "Player 3", 150)

	rank, exists := lb.GetRank("p2")
	if !exists {
		t.Fatal("Expected to find p2")
	}
	if rank != 1 {
		t.Errorf("Expected rank 1 for highest score, got %d", rank)
	}

	rank, exists = lb.GetRank("p1")
	if !exists {
		t.Fatal("Expected to find p1")
	}
	if rank != 3 {
		t.Errorf("Expected rank 3 for lowest score, got %d", rank)
	}

	rank, exists = lb.GetRank("p3")
	if !exists {
		t.Fatal("Expected to find p3")
	}
	if rank != 2 {
		t.Errorf("Expected rank 2 for middle score, got %d", rank)
	}
}

func TestGetRankAscending(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{Ascending: true})
	lb.AddOrUpdate("p1", "Player 1", 100)
	lb.AddOrUpdate("p2", "Player 2", 200)
	lb.AddOrUpdate("p3", "Player 3", 150)

	rank, exists := lb.GetRank("p1")
	if !exists {
		t.Fatal("Expected to find p1")
	}
	if rank != 1 {
		t.Errorf("Expected rank 1 for lowest score (ascending), got %d", rank)
	}
}

func TestGetTopN(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{})
	lb.AddOrUpdate("p1", "Player 1", 100)
	lb.AddOrUpdate("p2", "Player 2", 200)
	lb.AddOrUpdate("p3", "Player 3", 150)
	lb.AddOrUpdate("p4", "Player 4", 250)

	top2 := lb.GetTopN(2)
	if len(top2) != 2 {
		t.Fatalf("Expected 2 entries, got %d", len(top2))
	}

	if top2[0].ID != "p4" {
		t.Errorf("Expected p4 as top 1, got %s", top2[0].ID)
	}
	if top2[0].Rank != 1 {
		t.Errorf("Expected rank 1, got %d", top2[0].Rank)
	}
	if top2[1].ID != "p2" {
		t.Errorf("Expected p2 as top 2, got %s", top2[1].ID)
	}

	// Request more than available
	top10 := lb.GetTopN(10)
	if len(top10) != 4 {
		t.Errorf("Expected 4 entries, got %d", len(top10))
	}
}

func TestGetAroundRank(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{})
	for i := 1; i <= 10; i++ {
		lb.AddOrUpdate(string(rune('a'+i-1)), "Player", float64(i*10))
	}

	around := lb.GetAroundRank(5, 2, 2) // Rank 5, 2 before, 2 after
	if len(around) != 5 {
		t.Fatalf("Expected 5 entries, got %d", len(around))
	}

	// Should get ranks 3, 4, 5, 6, 7
	expectedRanks := []int{3, 4, 5, 6, 7}
	for i, entry := range around {
		if entry.Rank != expectedRanks[i] {
			t.Errorf("Expected rank %d, got %d", expectedRanks[i], entry.Rank)
		}
	}
}

func TestGetRange(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{})
	for i := 1; i <= 10; i++ {
		lb.AddOrUpdate(string(rune('a'+i-1)), "Player", float64(i*10))
	}

	entries := lb.GetRange(3, 6) // Ranks 3-6
	if len(entries) != 4 {
		t.Fatalf("Expected 4 entries, got %d", len(entries))
	}

	expectedRanks := []int{3, 4, 5, 6}
	for i, entry := range entries {
		if entry.Rank != expectedRanks[i] {
			t.Errorf("Expected rank %d, got %d", expectedRanks[i], entry.Rank)
		}
	}
}

func TestGetPercentile(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{})
	for i := 1; i <= 10; i++ {
		lb.AddOrUpdate(string(rune('a'+i-1)), "Player", float64(i*10))
	}

	percentile, exists := lb.GetPercentile("j") // Score 100, rank 1 (highest)
	if !exists {
		t.Fatal("Expected to find entry")
	}
	// For descending order, rank 1 gives percentile = (10-1+1)/10 = 100%
	if percentile != 100 {
		t.Errorf("Expected percentile 100 for top rank, got %f", percentile)
	}

	percentile, exists = lb.GetPercentile("a") // Score 10, rank 10 (lowest)
	if !exists {
		t.Fatal("Expected to find entry")
	}
	// For descending order, rank 10 gives percentile = (10-10+1)/10 = 10%
	if percentile != 10 {
		t.Errorf("Expected percentile 10 for bottom rank, got %f", percentile)
	}
}

func TestGetScoreAtPercentile(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{})
	for i := 1; i <= 10; i++ {
		lb.AddOrUpdate(string(rune('a'+i-1)), "Player", float64(i*10))
	}

	// 0th percentile should be the highest score (rank 1)
	score := lb.GetScoreAtPercentile(0)
	if score != 100 {
		t.Errorf("Expected score 100 at 0th percentile, got %f", score)
	}

	// 100th percentile should be the lowest score
	score = lb.GetScoreAtPercentile(100)
	if score != 10 {
		t.Errorf("Expected score 10 at 100th percentile, got %f", score)
	}
}

func TestMaxSize(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{MaxSize: 3})
	lb.AddOrUpdate("p1", "Player 1", 100)
	lb.AddOrUpdate("p2", "Player 2", 200)
	lb.AddOrUpdate("p3", "Player 3", 150)
	lb.AddOrUpdate("p4", "Player 4", 50) // Should evict lowest (p4 would be lowest)

	if lb.Count() != 3 {
		t.Errorf("Expected 3 entries with MaxSize=3, got %d", lb.Count())
	}

	// p1 (100) should have been evicted when p4 (50) was added
	_, exists := lb.GetEntry("p1")
	if exists {
		t.Error("Expected p1 to be evicted")
	}
}

func TestMerge(t *testing.T) {
	lb1 := NewLeaderboard(LeaderboardConfig{})
	lb1.AddOrUpdate("p1", "Player 1", 100)
	lb1.AddOrUpdate("p2", "Player 2", 200)

	lb2 := NewLeaderboard(LeaderboardConfig{})
	lb2.AddOrUpdate("p2", "Player 2", 300) // Higher score for p2
	lb2.AddOrUpdate("p3", "Player 3", 150)

	lb1.Merge(lb2)

	if lb1.Count() != 3 {
		t.Errorf("Expected 3 entries after merge, got %d", lb1.Count())
	}

	entry, _ := lb1.GetEntry("p2")
	if entry.Score != 300 {
		t.Errorf("Expected merged score 300, got %f", entry.Score)
	}
}

func TestGetStats(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{})
	for i := 1; i <= 5; i++ {
		lb.AddOrUpdate(string(rune('a'+i-1)), "Player", float64(i*10))
	}

	stats := lb.GetStats()
	if stats.Count != 5 {
		t.Errorf("Expected count 5, got %d", stats.Count)
	}
	if stats.MaxScore != 50 {
		t.Errorf("Expected max 50, got %f", stats.MaxScore)
	}
	if stats.MinScore != 10 {
		t.Errorf("Expected min 10, got %f", stats.MinScore)
	}
	if stats.AvgScore != 30 {
		t.Errorf("Expected avg 30, got %f", stats.AvgScore)
	}
	if stats.MedianScore != 30 {
		t.Errorf("Expected median 30, got %f", stats.MedianScore)
	}
}

func TestClear(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{})
	lb.AddOrUpdate("p1", "Player 1", 100)
	lb.Clear()

	if lb.Count() != 0 {
		t.Errorf("Expected empty leaderboard after clear, got %d entries", lb.Count())
	}
}

func TestLeaderboardHeap(t *testing.T) {
	h := NewLeaderboardHeap(false) // Descending (max-heap behavior)

	h.Add(&Entry{ID: "p1", Name: "Player 1", Score: 100})
	h.Add(&Entry{ID: "p2", Name: "Player 2", Score: 200})
	h.Add(&Entry{ID: "p3", Name: "Player 3", Score: 150})

	top := h.PeekTop()
	if top == nil {
		t.Fatal("Expected non-nil top entry")
	}

	sorted := h.GetSorted()
	if len(sorted) != 3 {
		t.Fatalf("Expected 3 sorted entries, got %d", len(sorted))
	}
	if sorted[0].Score != 200 {
		t.Errorf("Expected top score 200, got %f", sorted[0].Score)
	}
	if sorted[0].Rank != 1 {
		t.Errorf("Expected rank 1, got %d", sorted[0].Rank)
	}
}

func TestLeaderboardHeapPop(t *testing.T) {
	h := NewLeaderboardHeap(false)
	h.Add(&Entry{ID: "p1", Name: "Player 1", Score: 100})
	h.Add(&Entry{ID: "p2", Name: "Player 2", Score: 200})

	popped := h.PopTop()
	if popped == nil {
		t.Fatal("Expected non-nil popped entry")
	}
	if popped.Score != 100 { // Min-heap, so 100 pops first
		t.Errorf("Expected popped score 100, got %f", popped.Score)
	}
}

func TestTieBreakAlphabetical(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{})
	lb.AddOrUpdate("p1", "Zoe", 100)
	lb.AddOrUpdate("p2", "Alice", 100)
	lb.AddOrUpdate("p3", "Bob", 100)

	// All have same score, should be ranked alphabetically by name
	rank1, _ := lb.GetRankWithTieBreak("p2", TieBreakAlphabetical) // Alice
	_, _ = lb.GetRankWithTieBreak("p3", TieBreakReverseAlphabetical) // Bob
	rank3, _ := lb.GetRankWithTieBreak("p1", TieBreakAlphabetical) // Zoe

	if rank1 != 1 {
		t.Errorf("Expected Alice at rank 1, got %d", rank1)
	}
	if rank3 != 3 {
		t.Errorf("Expected Zoe at rank 3, got %d", rank3)
	}
}

func TestGetAroundID(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{})
	for i := 1; i <= 10; i++ {
		lb.AddOrUpdate(string(rune('a'+i-1)), "Player", float64(i*10))
	}

	// Get entries around "e" (rank 6, score 60)
	around := lb.GetAroundID("e", 2, 2)
	if around == nil {
		t.Fatal("Expected non-nil result")
	}
	if len(around) != 5 {
		t.Errorf("Expected 5 entries, got %d", len(around))
	}
}

func TestConcurrentAccess(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{})
	done := make(chan bool)

	// Concurrent writes
	for i := 0; i < 10; i++ {
		go func(id int) {
			for j := 0; j < 100; j++ {
				lb.AddOrUpdate(string(rune('a'+id)), "Player", float64(j))
			}
			done <- true
		}(i)
	}

	// Concurrent reads
	for i := 0; i < 5; i++ {
		go func() {
			for j := 0; j < 100; j++ {
				lb.GetTopN(5)
				lb.GetStats()
			}
			done <- true
		}()
	}

	// Wait for all goroutines
	for i := 0; i < 15; i++ {
		<-done
	}
}

func TestEmptyLeaderboard(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{})

	if lb.Count() != 0 {
		t.Error("Expected empty leaderboard")
	}

	top := lb.GetTopN(5)
	if len(top) != 0 {
		t.Errorf("Expected empty top entries, got %d", len(top))
	}

	stats := lb.GetStats()
	if stats.Count != 0 {
		t.Errorf("Expected count 0, got %d", stats.Count)
	}

	_, exists := lb.GetRank("nonexistent")
	if exists {
		t.Error("Expected entry not to exist")
	}
}

func TestNegativeScores(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{})
	lb.AddOrUpdate("p1", "Player 1", -100)
	lb.AddOrUpdate("p2", "Player 2", -50)
	lb.AddOrUpdate("p3", "Player 3", 0)

	top := lb.GetTopN(3)
	if top[0].Score != 0 {
		t.Errorf("Expected highest score 0, got %f", top[0].Score)
	}
	if top[2].Score != -100 {
		t.Errorf("Expected lowest score -100, got %f", top[2].Score)
	}
}

func TestFloatingPointPrecision(t *testing.T) {
	lb := NewLeaderboard(LeaderboardConfig{})
	lb.AddOrUpdate("p1", "Player 1", 100.123456789)
	lb.AddOrUpdate("p2", "Player 2", 100.123456788)

	entry, _ := lb.GetEntry("p1")
	if math.Abs(entry.Score-100.123456789) > 1e-9 {
		t.Errorf("Floating point precision lost: %f", entry.Score)
	}
}