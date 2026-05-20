package weightedroundrobin

import (
	"fmt"
	"sync"
	"sync/atomic"
	"testing"
)

func TestWeightedRoundRobin(t *testing.T) {
	backends := []*Backend{
		NewBackend("a", 5),
		NewBackend("b", 3),
		NewBackend("c", 2),
	}

	wrr, err := NewWeightedRoundRobin(backends)
	if err != nil {
		t.Fatalf("NewWeightedRoundRobin failed: %v", err)
	}

	// Test distribution over 100 selections
	counts := make(map[string]int)
	for i := 0; i < 100; i++ {
		selected := wrr.Select()
		counts[selected.Name]++
	}

	// With weights 5:3:2, over 100 selections we expect roughly 50:30:20
	// Allow some variance
	if counts["a"] < 40 || counts["a"] > 60 {
		t.Errorf("Expected 'a' count ~50, got %d", counts["a"])
	}
	if counts["b"] < 20 || counts["b"] > 40 {
		t.Errorf("Expected 'b' count ~30, got %d", counts["b"])
	}
	if counts["c"] < 10 || counts["c"] > 30 {
		t.Errorf("Expected 'c' count ~20, got %d", counts["c"])
	}

	t.Logf("Distribution: a=%d, b=%d, c=%d", counts["a"], counts["b"], counts["c"])
}

func TestWeightedRoundRobin_EqualWeights(t *testing.T) {
	backends := []*Backend{
		NewBackend("a", 1),
		NewBackend("b", 1),
		NewBackend("c", 1),
	}

	wrr, err := NewWeightedRoundRobin(backends)
	if err != nil {
		t.Fatalf("NewWeightedRoundRobin failed: %v", err)
	}

	counts := make(map[string]int)
	for i := 0; i < 30; i++ {
		selected := wrr.Select()
		counts[selected.Name]++
	}

	// With equal weights, each should get ~10 selections
	for name, count := range counts {
		if count < 7 || count > 13 {
			t.Errorf("Expected %s count ~10, got %d", name, count)
		}
	}
}

func TestWeightedRoundRobin_InvalidInput(t *testing.T) {
	_, err := NewWeightedRoundRobin(nil)
	if err == nil {
		t.Error("Expected error for nil backends")
	}

	_, err = NewWeightedRoundRobin([]*Backend{})
	if err == nil {
		t.Error("Expected error for empty backends")
	}

	_, err = NewWeightedRoundRobin([]*Backend{NewBackend("a", 0)})
	if err == nil {
		t.Error("Expected error for zero weight")
	}
}

func TestSmoothWeightedRoundRobin(t *testing.T) {
	backends := []*Backend{
		NewBackend("a", 5),
		NewBackend("b", 1),
		NewBackend("c", 1),
	}

	swrr, err := NewSmoothWeightedRoundRobin(backends)
	if err != nil {
		t.Fatalf("NewSmoothWeightedRoundRobin failed: %v", err)
	}

	// Test smooth distribution pattern
	// For weights [5, 1, 1], 7 selections should be: a a a a a b c (in smooth order)
	sequence := make([]string, 14)
	for i := 0; i < 14; i++ {
		sequence[i] = swrr.Select().Name
	}

	t.Logf("Selection sequence: %v", sequence)

	// Count distribution
	counts := make(map[string]int)
	for _, name := range sequence {
		counts[name]++
	}

	// Expected: a=10, b=2, c=2 (within one cycle of 7)
	if counts["a"] != 10 {
		t.Errorf("Expected 'a' count 10, got %d", counts["a"])
	}
	if counts["b"] != 2 {
		t.Errorf("Expected 'b' count 2, got %d", counts["b"])
	}
	if counts["c"] != 2 {
		t.Errorf("Expected 'c' count 2, got %d", counts["c"])
	}
}

func TestSmoothWeightedRoundRobin_Distribution(t *testing.T) {
	backends := []*Backend{
		NewBackend("heavy", 10),
		NewBackend("medium", 5),
		NewBackend("light", 1),
	}

	swrr, err := NewSmoothWeightedRoundRobin(backends)
	if err != nil {
		t.Fatalf("NewSmoothWeightedRoundRobin failed: %v", err)
	}

	counts := make(map[string]int)
	for i := 0; i < 160; i++ { // 10 iterations of 16-weight cycle
		selected := swrr.Select()
		counts[selected.Name]++
	}

	// Distribution should be proportional to weights
	// heavy: 100, medium: 50, light: 10
	t.Logf("Distribution: heavy=%d, medium=%d, light=%d", counts["heavy"], counts["medium"], counts["light"])

	// Allow 10% variance
	if counts["heavy"] < 90 || counts["heavy"] > 110 {
		t.Errorf("Expected heavy count ~100, got %d", counts["heavy"])
	}
}

func TestWeightedRandom(t *testing.T) {
	backends := []*Backend{
		NewBackend("a", 4),
		NewBackend("b", 2),
		NewBackend("c", 1),
	}

	wr, err := NewWeightedRandom(backends)
	if err != nil {
		t.Fatalf("NewWeightedRandom failed: %v", err)
	}

	// Test distribution over many selections
	counts := make(map[string]int)
	iterations := 7000
	for i := 0; i < iterations; i++ {
		selected := wr.Select()
		counts[selected.Name]++
	}

	// With weights 4:2:1, expected distribution:
	// a: ~4000, b: ~2000, c: ~1000
	t.Logf("Distribution: a=%d, b=%d, c=%d", counts["a"], counts["b"], counts["c"])

	// Allow 15% variance due to randomness
	if counts["a"] < 3400 || counts["a"] > 4600 {
		t.Errorf("Expected 'a' count ~4000, got %d", counts["a"])
	}
	if counts["b"] < 1700 || counts["b"] > 2300 {
		t.Errorf("Expected 'b' count ~2000, got %d", counts["b"])
	}
	if counts["c"] < 850 || counts["c"] > 1150 {
		t.Errorf("Expected 'c' count ~1000, got %d", counts["c"])
	}
}

func TestWeightedRandom_InvalidInput(t *testing.T) {
	_, err := NewWeightedRandom([]*Backend{})
	if err == nil {
		t.Error("Expected error for empty backends")
	}

	_, err = NewWeightedRandom([]*Backend{NewBackend("a", -1)})
	if err == nil {
		t.Error("Expected error for negative weight")
	}
}

func TestLeastConnections(t *testing.T) {
	backends := []*Backend{
		NewBackend("a", 1),
		NewBackend("b", 1),
		NewBackend("c", 1),
	}

	lc, err := NewLeastConnections(backends)
	if err != nil {
		t.Fatalf("NewLeastConnections failed: %v", err)
	}

	// Initially all have 0 connections, should pick first
	selected := lc.Select()
	if selected.Name != "a" {
		t.Errorf("Expected first backend 'a', got %s", selected.Name)
	}

	// Increment connection for 'a'
	atomic.AddInt64(&backends[0].Connections, 5)

	// Now should pick 'b' or 'c' (both have 0)
	selected = lc.Select()
	if selected.Name == "a" {
		t.Error("Should not pick 'a' which has more connections")
	}

	// Add connection to 'b'
	atomic.AddInt64(&backends[1].Connections, 1)

	// Should pick 'c' with 0 connections
	selected = lc.Select()
	if selected.Name != "c" {
		t.Errorf("Expected 'c' with least connections, got %s", selected.Name)
	}
}

func TestLeastConnections_Concurrent(t *testing.T) {
	backends := []*Backend{
		NewBackend("a", 1),
		NewBackend("b", 1),
		NewBackend("c", 1),
	}

	lc, err := NewLeastConnections(backends)
	if err != nil {
		t.Fatalf("NewLeastConnections failed: %v", err)
	}

	var wg sync.WaitGroup
	counts := make(map[string]int64)
	var countsMu sync.Mutex

	// Simulate 100 concurrent selections
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			selected := lc.Select()
			selected.Incr()
			countsMu.Lock()
			counts[selected.Name]++
			countsMu.Unlock()
		}()
	}

	wg.Wait()

	t.Logf("Concurrent selection distribution: %v", counts)
}

func TestLeastConnections_AddRemove(t *testing.T) {
	backends := []*Backend{
		NewBackend("a", 1),
		NewBackend("b", 1),
	}

	lc, err := NewLeastConnections(backends)
	if err != nil {
		t.Fatalf("NewLeastConnections failed: %v", err)
	}

	// Add new backend
	newBackend := NewBackend("c", 1)
	err = lc.AddBackend(newBackend)
	if err != nil {
		t.Errorf("AddBackend failed: %v", err)
	}

	// Try to add backend with invalid weight
	err = lc.AddBackend(NewBackend("d", 0))
	if err == nil {
		t.Error("Expected error for zero weight backend")
	}

	// Remove backend
	removed := lc.RemoveBackend("b")
	if !removed {
		t.Error("RemoveBackend should return true for existing backend")
	}

	removed = lc.RemoveBackend("nonexistent")
	if removed {
		t.Error("RemoveBackend should return false for non-existent backend")
	}
}

func TestWeightedLeastConnections(t *testing.T) {
	backends := []*Backend{
		NewBackend("a", 5), // High weight
		NewBackend("b", 1), // Low weight
		NewBackend("c", 1), // Low weight
	}

	wlc, err := NewWeightedLeastConnections(backends)
	if err != nil {
		t.Fatalf("NewWeightedLeastConnections failed: %v", err)
	}

	// All have 0 connections, should pick first
	selected := wlc.Select()
	if selected.Name != "a" {
		t.Errorf("Expected 'a', got %s", selected.Name)
	}

	// Add connections
	atomic.AddInt64(&backends[0].Connections, 10) // a: 10/5 = 2.0
	atomic.AddInt64(&backends[1].Connections, 1)  // b: 1/1 = 1.0
	atomic.AddInt64(&backends[2].Connections, 0)  // c: 0/1 = 0.0

	selected = wlc.Select()
	if selected.Name != "c" {
		t.Errorf("Expected 'c' with lowest ratio, got %s", selected.Name)
	}

	// Verify GetBackends
	allBackends := wlc.GetBackends()
	if len(allBackends) != 3 {
		t.Errorf("Expected 3 backends, got %d", len(allBackends))
	}
}

func TestPowerOfTwoChoices(t *testing.T) {
	backends := []*Backend{
		NewBackend("a", 1),
		NewBackend("b", 1),
		NewBackend("c", 1),
		NewBackend("d", 1),
	}

	p2c, err := NewPowerOfTwoChoices(backends)
	if err != nil {
		t.Fatalf("NewPowerOfTwoChoices failed: %v", err)
	}

	// Test that it selects backends
	counts := make(map[string]int)
	for i := 0; i < 1000; i++ {
		selected := p2c.Select()
		counts[selected.Name]++
	}

	// With power of two choices, distribution should be roughly even
	t.Logf("Power of two choices distribution: %v", counts)

	for name, count := range counts {
		if count < 150 || count > 350 {
			t.Errorf("Backend %s has unusual count: %d", name, count)
		}
	}
}

func TestPowerOfTwoChoices_ConnectionAware(t *testing.T) {
	backends := []*Backend{
		NewBackend("a", 1),
		NewBackend("b", 1),
		NewBackend("c", 1),
	}

	p2c, err := NewPowerOfTwoChoices(backends)
	if err != nil {
		t.Fatalf("NewPowerOfTwoChoices failed: %v", err)
	}

	// Add many connections to 'a'
	for i := 0; i < 10; i++ {
		atomic.AddInt64(&backends[0].Connections, 1)
	}

	// Over many selections, 'a' should rarely be picked
	counts := make(map[string]int)
	for i := 0; i < 100; i++ {
		selected := p2c.Select()
		counts[selected.Name]++
	}

	// 'a' should have significantly fewer selections
	t.Logf("Distribution with high connections on 'a': %v", counts)
	if counts["a"] > 50 {
		t.Errorf("'a' with high connections should be selected less, got %d", counts["a"])
	}
}

func TestPowerOfTwoChoices_InvalidInput(t *testing.T) {
	_, err := NewPowerOfTwoChoices([]*Backend{NewBackend("a", 1)})
	if err == nil {
		t.Error("Expected error for single backend")
	}

	_, err = NewPowerOfTwoChoices([]*Backend{})
	if err == nil {
		t.Error("Expected error for empty backends")
	}
}

func TestBackend_Connections(t *testing.T) {
	b := NewBackend("test", 5)

	if b.GetConnections() != 0 {
		t.Errorf("Expected 0 connections, got %d", b.GetConnections())
	}

	b.Incr()
	if b.GetConnections() != 1 {
		t.Errorf("Expected 1 connection, got %d", b.GetConnections())
	}

	b.Incr()
	b.Incr()
	if b.GetConnections() != 3 {
		t.Errorf("Expected 3 connections, got %d", b.GetConnections())
	}

	b.Decr()
	if b.GetConnections() != 2 {
		t.Errorf("Expected 2 connections, got %d", b.GetConnections())
	}
}

func TestConcurrentSelection(t *testing.T) {
	backends := []*Backend{
		NewBackend("a", 5),
		NewBackend("b", 3),
		NewBackend("c", 2),
	}

	wrr, _ := NewWeightedRoundRobin(backends)
	swrr, _ := NewSmoothWeightedRoundRobin(backends)
	wr, _ := NewWeightedRandom(backends)
	lc, _ := NewLeastConnections(backends)

	var wg sync.WaitGroup
	selectors := []struct {
		name string
		fn   func() *Backend
	}{
		{"WRR", wrr.Select},
		{"SWRR", swrr.Select},
		{"WR", wr.Select},
		{"LC", lc.Select},
	}

	for _, s := range selectors {
		wg.Add(1)
		go func(name string, fn func() *Backend) {
			defer wg.Done()
			for i := 0; i < 100; i++ {
				selected := fn()
				if selected == nil {
					t.Errorf("%s returned nil backend", name)
				}
			}
		}(s.name, s.fn)
	}

	wg.Wait()
}

// Benchmark tests
func BenchmarkWeightedRoundRobin_Select(b *testing.B) {
	backends := []*Backend{
		NewBackend("a", 5),
		NewBackend("b", 3),
		NewBackend("c", 2),
	}
	wrr, _ := NewWeightedRoundRobin(backends)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		wrr.Select()
	}
}

func BenchmarkSmoothWeightedRoundRobin_Select(b *testing.B) {
	backends := []*Backend{
		NewBackend("a", 5),
		NewBackend("b", 3),
		NewBackend("c", 2),
	}
	swrr, _ := NewSmoothWeightedRoundRobin(backends)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		swrr.Select()
	}
}

func BenchmarkWeightedRandom_Select(b *testing.B) {
	backends := []*Backend{
		NewBackend("a", 5),
		NewBackend("b", 3),
		NewBackend("c", 2),
	}
	wr, _ := NewWeightedRandom(backends)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		wr.Select()
	}
}

func BenchmarkLeastConnections_Select(b *testing.B) {
	backends := []*Backend{
		NewBackend("a", 1),
		NewBackend("b", 1),
		NewBackend("c", 1),
	}
	lc, _ := NewLeastConnections(backends)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		lc.Select()
	}
}

func BenchmarkPowerOfTwoChoices_Select(b *testing.B) {
	backends := []*Backend{
		NewBackend("a", 1),
		NewBackend("b", 1),
		NewBackend("c", 1),
		NewBackend("d", 1),
	}
	p2c, _ := NewPowerOfTwoChoices(backends)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		p2c.Select()
	}
}

// Example tests
func ExampleWeightedRoundRobin() {
	backends := []*Backend{
		NewBackend("server1", 5),
		NewBackend("server2", 3),
		NewBackend("server3", 2),
	}

	wrr, _ := NewWeightedRoundRobin(backends)

	// Select backends
	for i := 0; i < 10; i++ {
		selected := wrr.Select()
		fmt.Printf("Selected: %s\n", selected.Name)
	}
}

func ExampleSmoothWeightedRoundRobin() {
	backends := []*Backend{
		NewBackend("high-weight", 5),
		NewBackend("low-weight", 1),
	}

	swrr, _ := NewSmoothWeightedRoundRobin(backends)

	// The smooth algorithm distributes selections more evenly
	counts := make(map[string]int)
	for i := 0; i < 6; i++ {
		selected := swrr.Select()
		counts[selected.Name]++
	}

	// With weights 5:1, over 6 selections we expect 5 high-weight and 1 low-weight
	fmt.Printf("high-weight: %d, low-weight: %d\n", counts["high-weight"], counts["low-weight"])
	// Output: high-weight: 5, low-weight: 1
}

func ExampleLeastConnections() {
	backends := []*Backend{
		NewBackend("server1", 1),
		NewBackend("server2", 1),
		NewBackend("server3", 1),
	}

	lc, _ := NewLeastConnections(backends)

	// Simulate connection tracking
	selected := lc.Select()
	selected.Incr() // Simulate connection

	// Release connection later
	selected.Decr()

	fmt.Printf("Selected server: %s\n", selected.Name)
}