// Package leaderboard_utils provides efficient leaderboard and ranking utilities.
// It supports multiple ranking strategies, score updates, and leaderboard queries.
package leaderboard_utils

import (
	"container/heap"
	"sort"
	"sync"
)

// Entry represents a single leaderboard entry
type Entry struct {
	ID    string  // Unique identifier for the entry
	Name  string  // Display name
	Score float64 // Score value
	Rank  int     // Current rank (0 means unranked)
}

// LeaderboardConfig holds configuration for the leaderboard
type LeaderboardConfig struct {
	// MaxSize limits the number of entries stored (0 = unlimited)
	MaxSize int
	// Ascending determines sort order (false = highest first)
	Ascending bool
}

// Leaderboard manages a collection of ranked entries
type Leaderboard struct {
	mu       sync.RWMutex
	entries  map[string]*Entry
	config   LeaderboardConfig
	sorted   []*Entry
	dirty    bool
}

// NewLeaderboard creates a new leaderboard with the given configuration
func NewLeaderboard(config LeaderboardConfig) *Leaderboard {
	return &Leaderboard{
		entries: make(map[string]*Entry),
		config:  config,
	}
}

// AddOrUpdate adds a new entry or updates an existing one
func (lb *Leaderboard) AddOrUpdate(id, name string, score float64) {
	lb.mu.Lock()
	defer lb.mu.Unlock()

	if entry, exists := lb.entries[id]; exists {
		entry.Score = score
		entry.Name = name
	} else {
		if lb.config.MaxSize > 0 && len(lb.entries) >= lb.config.MaxSize {
			// Remove lowest/highest based on sort order
			lb.sort()
			removeIdx := len(lb.sorted) - 1
			if lb.config.Ascending {
				removeIdx = 0
			}
			if removeIdx >= 0 && removeIdx < len(lb.sorted) {
				delete(lb.entries, lb.sorted[removeIdx].ID)
			}
		}
		lb.entries[id] = &Entry{
			ID:    id,
			Name:  name,
			Score: score,
		}
	}
	lb.dirty = true
}

// Remove deletes an entry from the leaderboard
func (lb *Leaderboard) Remove(id string) bool {
	lb.mu.Lock()
	defer lb.mu.Unlock()

	if _, exists := lb.entries[id]; exists {
		delete(lb.entries, id)
		lb.dirty = true
		return true
	}
	return false
}

// GetEntry retrieves an entry by ID
func (lb *Leaderboard) GetEntry(id string) (*Entry, bool) {
	lb.mu.RLock()
	defer lb.mu.RUnlock()

	entry, exists := lb.entries[id]
	if !exists {
		return nil, false
	}
	
	// Make a copy with updated rank
	lb.sort()
	copy := *entry
	copy.Rank = lb.getRank(id)
	return &copy, true
}

// GetRank returns the rank of an entry by ID
func (lb *Leaderboard) GetRank(id string) (int, bool) {
	lb.mu.RLock()
	defer lb.mu.RUnlock()

	if _, exists := lb.entries[id]; !exists {
		return 0, false
	}
	
	lb.sort()
	return lb.getRank(id), true
}

// getRank is an internal method that assumes lock is held
func (lb *Leaderboard) getRank(id string) int {
	for i, e := range lb.sorted {
		if e.ID == id {
			return i + 1
		}
	}
	return 0
}

// GetTopN returns the top N entries
func (lb *Leaderboard) GetTopN(n int) []*Entry {
	lb.mu.RLock()
	defer lb.mu.RUnlock()

	lb.sort()

	if n > len(lb.sorted) {
		n = len(lb.sorted)
	}

	result := make([]*Entry, n)
	for i := 0; i < n; i++ {
		copy := *lb.sorted[i]
		copy.Rank = i + 1
		result[i] = &copy
	}
	return result
}

// GetAroundRank returns entries around a specific rank (useful for "near me" views)
func (lb *Leaderboard) GetAroundRank(rank, before, after int) []*Entry {
	lb.mu.RLock()
	defer lb.mu.RUnlock()

	lb.sort()

	start := rank - 1 - before
	if start < 0 {
		start = 0
	}

	end := rank + after
	if end > len(lb.sorted) {
		end = len(lb.sorted)
	}

	result := make([]*Entry, 0, end-start)
	for i := start; i < end; i++ {
		copy := *lb.sorted[i]
		copy.Rank = i + 1
		result = append(result, &copy)
	}
	return result
}

// GetAroundID returns entries around a specific entry ID
func (lb *Leaderboard) GetAroundID(id string, before, after int) []*Entry {
	lb.mu.RLock()
	defer lb.mu.RUnlock()

	if _, exists := lb.entries[id]; !exists {
		return nil
	}

	lb.sort()
	rank := lb.getRank(id)
	return lb.GetAroundRank(rank, before, after)
}

// GetRange returns entries within a rank range [start, end] (1-indexed)
func (lb *Leaderboard) GetRange(start, end int) []*Entry {
	lb.mu.RLock()
	defer lb.mu.RUnlock()

	lb.sort()

	if start < 1 {
		start = 1
	}
	if end > len(lb.sorted) {
		end = len(lb.sorted)
	}

	result := make([]*Entry, 0, end-start+1)
	for i := start - 1; i < end; i++ {
		copy := *lb.sorted[i]
		copy.Rank = i + 1
		result = append(result, &copy)
	}
	return result
}

// Count returns the number of entries
func (lb *Leaderboard) Count() int {
	lb.mu.RLock()
	defer lb.mu.RUnlock()
	return len(lb.entries)
}

// Clear removes all entries
func (lb *Leaderboard) Clear() {
	lb.mu.Lock()
	defer lb.mu.Unlock()
	lb.entries = make(map[string]*Entry)
	lb.sorted = nil
	lb.dirty = false
}

// sort updates the sorted slice if dirty
func (lb *Leaderboard) sort() {
	if !lb.dirty {
		return
	}

	lb.sorted = make([]*Entry, 0, len(lb.entries))
	for _, e := range lb.entries {
		lb.sorted = append(lb.sorted, e)
	}

	if lb.config.Ascending {
		sort.Slice(lb.sorted, func(i, j int) bool {
			return lb.sorted[i].Score < lb.sorted[j].Score
		})
	} else {
		sort.Slice(lb.sorted, func(i, j int) bool {
			return lb.sorted[i].Score > lb.sorted[j].Score
		})
	}

	lb.dirty = false
}

// GetPercentile returns the percentile rank of an entry (0-100)
func (lb *Leaderboard) GetPercentile(id string) (float64, bool) {
	lb.mu.RLock()
	defer lb.mu.RUnlock()

	if _, exists := lb.entries[id]; !exists {
		return 0, false
	}

	lb.sort()
	rank := lb.getRank(id)
	total := len(lb.sorted)
	
	if total == 0 {
		return 0, true
	}

	if lb.config.Ascending {
		return float64(rank) / float64(total) * 100, true
	}
	return float64(total-rank+1) / float64(total) * 100, true
}

// GetScoreAtPercentile returns the score at a given percentile
func (lb *Leaderboard) GetScoreAtPercentile(percentile float64) float64 {
	lb.mu.RLock()
	defer lb.mu.RUnlock()

	lb.sort()
	total := len(lb.sorted)
	if total == 0 {
		return 0
	}

	index := int(float64(total-1) * percentile / 100)
	if index < 0 {
		index = 0
	}
	if index >= total {
		index = total - 1
	}

	return lb.sorted[index].Score
}

// Merge combines another leaderboard into this one
func (lb *Leaderboard) Merge(other *Leaderboard) {
	lb.mu.Lock()
	defer lb.mu.Unlock()

	other.mu.RLock()
	defer other.mu.RUnlock()

	for id, entry := range other.entries {
		if existing, exists := lb.entries[id]; exists {
			// Merge strategy: keep higher score
			if (!lb.config.Ascending && entry.Score > existing.Score) ||
				(lb.config.Ascending && entry.Score < existing.Score) {
				existing.Score = entry.Score
			}
		} else {
			lb.entries[id] = &Entry{
				ID:    entry.ID,
				Name:  entry.Name,
				Score: entry.Score,
			}
		}
	}
	lb.dirty = true
}

// GetStats returns statistics about the leaderboard
func (lb *Leaderboard) GetStats() LeaderboardStats {
	lb.mu.RLock()
	defer lb.mu.RUnlock()

	lb.sort()

	stats := LeaderboardStats{
		Count: len(lb.sorted),
	}

	if len(lb.sorted) == 0 {
		return stats
	}

	stats.MinScore = lb.sorted[len(lb.sorted)-1].Score
	stats.MaxScore = lb.sorted[0].Score
	if lb.config.Ascending {
		stats.MinScore = lb.sorted[0].Score
		stats.MaxScore = lb.sorted[len(lb.sorted)-1].Score
	}

	var sum float64
	for _, e := range lb.sorted {
		sum += e.Score
	}
	stats.AvgScore = sum / float64(len(lb.sorted))

	// Calculate median
	mid := len(lb.sorted) / 2
	if len(lb.sorted)%2 == 0 {
		stats.MedianScore = (lb.sorted[mid-1].Score + lb.sorted[mid].Score) / 2
	} else {
		stats.MedianScore = lb.sorted[mid].Score
	}

	return stats
}

// LeaderboardStats holds statistical information about a leaderboard
type LeaderboardStats struct {
	Count       int
	MinScore    float64
	MaxScore    float64
	AvgScore    float64
	MedianScore float64
}

// ==================== Priority Queue for Real-time Leaderboard ====================

// LeaderboardHeap is a min-heap implementation for efficient top-N queries
type LeaderboardHeap struct {
	entries   []*Entry
	ascending bool
}

func (h LeaderboardHeap) Len() int           { return len(h.entries) }
func (h LeaderboardHeap) Less(i, j int) bool { return h.entries[i].Score < h.entries[j].Score }
func (h LeaderboardHeap) Swap(i, j int)      { h.entries[i], h.entries[j] = h.entries[j], h.entries[i] }

func (h *LeaderboardHeap) Push(x interface{}) {
	h.entries = append(h.entries, x.(*Entry))
}

func (h *LeaderboardHeap) Pop() interface{} {
	old := h.entries
	n := len(old)
	x := old[n-1]
	h.entries = old[0 : n-1]
	return x
}

// NewLeaderboardHeap creates a new heap-based leaderboard
func NewLeaderboardHeap(ascending bool) *LeaderboardHeap {
	return &LeaderboardHeap{
		entries:   make([]*Entry, 0),
		ascending: ascending,
	}
}

// Add inserts an entry into the heap
func (h *LeaderboardHeap) Add(entry *Entry) {
	heap.Push(h, entry)
}

// PeekTop returns the top entry without removing it
func (h *LeaderboardHeap) PeekTop() *Entry {
	if len(h.entries) == 0 {
		return nil
	}
	return h.entries[0]
}

// PopTop removes and returns the top entry
func (h *LeaderboardHeap) PopTop() *Entry {
	if len(h.entries) == 0 {
		return nil
	}
	return heap.Pop(h).(*Entry)
}

// GetSorted returns all entries sorted
func (h *LeaderboardHeap) GetSorted() []*Entry {
	result := make([]*Entry, len(h.entries))
	copy(result, h.entries)
	
	if h.ascending {
		sort.Slice(result, func(i, j int) bool {
			return result[i].Score < result[j].Score
		})
	} else {
		sort.Slice(result, func(i, j int) bool {
			return result[i].Score > result[j].Score
		})
	}
	
	for i := range result {
		result[i].Rank = i + 1
	}
	return result
}

// ==================== Tie-Breaking Strategies ====================

// TieBreakStrategy defines how to handle ties
type TieBreakStrategy int

const (
	TieBreakNone TieBreakStrategy = iota
	TieBreakFirstCome
	TieBreakAlphabetical
	TieBreakReverseAlphabetical
)

// GetRankWithTieBreak returns rank with tie-breaking applied
func (lb *Leaderboard) GetRankWithTieBreak(id string, strategy TieBreakStrategy) (int, bool) {
	lb.mu.RLock()
	defer lb.mu.RUnlock()

	if _, exists := lb.entries[id]; !exists {
		return 0, false
	}

	lb.sort()

	// Group by score
	scoreGroups := make(map[float64][]*Entry)
	for _, e := range lb.sorted {
		scoreGroups[e.Score] = append(scoreGroups[e.Score], e)
	}

	// Sort within groups based on strategy
	for _, group := range scoreGroups {
		switch strategy {
		case TieBreakAlphabetical:
			sort.Slice(group, func(i, j int) bool {
				return group[i].Name < group[j].Name
			})
		case TieBreakReverseAlphabetical:
			sort.Slice(group, func(i, j int) bool {
				return group[i].Name > group[j].Name
			})
		}
	}

	// Rebuild sorted list with tie-break
	newSorted := make([]*Entry, 0, len(lb.sorted))
	if lb.config.Ascending {
		scores := make([]float64, 0)
		for s := range scoreGroups {
			scores = append(scores, s)
		}
		sort.Float64s(scores)
		for _, s := range scores {
			newSorted = append(newSorted, scoreGroups[s]...)
		}
	} else {
		scores := make([]float64, 0)
		for s := range scoreGroups {
			scores = append(scores, s)
		}
		sort.Sort(sort.Reverse(sort.Float64Slice(scores)))
		for _, s := range scores {
			newSorted = append(newSorted, scoreGroups[s]...)
		}
	}

	// Find rank
	for i, e := range newSorted {
		if e.ID == id {
			return i + 1, true
		}
	}
	return 0, false
}