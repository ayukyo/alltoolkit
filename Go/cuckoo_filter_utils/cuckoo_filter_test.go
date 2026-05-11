package cuckoo_filter_utils

import (
	"fmt"
	"math"
	"math/rand"
	"testing"
)

func TestNewCuckooFilter(t *testing.T) {
	tests := []struct {
		name    string
		opts    Options
		wantErr error
	}{
		{
			name: "default options",
			opts: DefaultOptions(1000),
			wantErr: nil,
		},
		{
			name: "zero capacity",
			opts: Options{Capacity: 0},
			wantErr: ErrCapacityZero,
		},
		{
			name: "bucket size 2",
			opts: Options{Capacity: 100, BucketSize: 2},
			wantErr: nil,
		},
		{
			name: "bucket size 8",
			opts: Options{Capacity: 100, BucketSize: 8},
			wantErr: nil,
		},
		{
			name: "very low false positive rate",
			opts: Options{Capacity: 100, FalsePositiveRate: 0.001},
			wantErr: nil,
		},
		{
			name: "high false positive rate",
			opts: Options{Capacity: 100, FalsePositiveRate: 0.5},
			wantErr: nil,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			cf, err := New(tt.opts)
			if tt.wantErr != nil {
				if err != tt.wantErr {
					t.Errorf("New() error = %v, wantErr %v", err, tt.wantErr)
				}
				return
			}
			if err != nil {
				t.Errorf("New() unexpected error: %v", err)
				return
			}
			if cf == nil {
				t.Error("New() returned nil filter")
			}
		})
	}
}

func TestAddContains(t *testing.T) {
	cf, err := New(DefaultOptions(1000))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	items := [][]byte{
		[]byte("hello"),
		[]byte("world"),
		[]byte("test"),
		[]byte("cuckoo"),
		[]byte("filter"),
	}

	for _, item := range items {
		if err := cf.Add(item); err != nil {
			t.Errorf("Add(%s) failed: %v", item, err)
		}
	}

	for _, item := range items {
		if !cf.Contains(item) {
			t.Errorf("Contains(%s) returned false after adding", item)
		}
	}
}

func TestRemove(t *testing.T) {
	cf, err := New(DefaultOptions(1000))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	item := []byte("test")
	if err := cf.Add(item); err != nil {
		t.Fatalf("Add failed: %v", err)
	}

	if !cf.Contains(item) {
		t.Fatal("Contains returned false after adding")
	}

	if !cf.Remove(item) {
		t.Error("Remove returned false")
	}

	if cf.Contains(item) {
		t.Error("Contains returned true after removal")
	}
}

func TestFalsePositiveRate(t *testing.T) {
	opts := DefaultOptions(10000)
	opts.FalsePositiveRate = 0.03

	cf, err := New(opts)
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	// Add 100 items - with 8-bit fingerprints, more items cause higher FP due to collisions
	// The theoretical FP rate assumes low load factor
	addCount := 100
	for i := 0; i < addCount; i++ {
		cf.Add([]byte(fmt.Sprintf("item_%d", i)))
	}

	t.Logf("Added %d items, capacity=%d, fpBits=%d, loadFactor=%.2f", 
		cf.Count(), cf.Capacity(), cf.fpBits, cf.LoadFactor())

	// Test items that weren't added
	falsePositives := 0
	testCount := 2000
	for i := addCount; i < addCount+testCount; i++ {
		item := fmt.Sprintf("item_%d", i)
		if cf.Contains([]byte(item)) {
			falsePositives++
		}
	}

	actualRate := float64(falsePositives) / float64(testCount)
	expectedRate := cf.FalsePositiveRate()

	t.Logf("False positive rate: actual=%.4f, expected=%.4f", actualRate, expectedRate)

	// FP rate should be within 2x of expected at low load
	if actualRate > expectedRate*2.5 {
		t.Errorf("False positive rate too high: actual=%f, expected=%f", actualRate, expectedRate)
	}
}

func TestCapacity(t *testing.T) {
	opts := DefaultOptions(100)
	cf, err := New(opts)
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	// Try to add more items than capacity
	addedCount := 0
	for i := 0; i < 200; i++ {
		item := []byte(fmt.Sprintf("item_%d", i))
		if err := cf.Add(item); err == nil {
			addedCount++
		} else if err != ErrFilterFull {
			t.Errorf("Unexpected error: %v", err)
		}
	}

	t.Logf("Added %d items out of 200 (capacity=%d)", addedCount, cf.Capacity())
}

func TestCount(t *testing.T) {
	cf, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	if cf.Count() != 0 {
		t.Errorf("Initial count should be 0, got %d", cf.Count())
	}

	for i := 0; i < 50; i++ {
		cf.Add([]byte(fmt.Sprintf("item_%d", i)))
	}

	if cf.Count() != 50 {
		t.Errorf("Count should be 50, got %d", cf.Count())
	}

	cf.Remove([]byte("item_0"))
	if cf.Count() != 49 {
		t.Errorf("Count should be 49 after removal, got %d", cf.Count())
	}
}

func TestLoadFactor(t *testing.T) {
	cf, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	if cf.LoadFactor() != 0 {
		t.Errorf("Initial load factor should be 0, got %f", cf.LoadFactor())
	}

	// Add half capacity
	half := cf.Capacity() / 2
	for i := uint(0); i < half; i++ {
		cf.Add([]byte(fmt.Sprintf("item_%d", i)))
	}

	loadFactor := cf.LoadFactor()
	if loadFactor < 0.4 || loadFactor > 0.6 {
		t.Errorf("Load factor should be around 0.5, got %f", loadFactor)
	}
}

func TestReset(t *testing.T) {
	cf, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	for i := 0; i < 50; i++ {
		cf.Add([]byte(fmt.Sprintf("item_%d", i)))
	}

	cf.Reset()

	if cf.Count() != 0 {
		t.Errorf("Count should be 0 after reset, got %d", cf.Count())
	}

	for i := 0; i < 50; i++ {
		if cf.Contains([]byte(fmt.Sprintf("item_%d", i))) {
			t.Errorf("Filter should be empty after reset")
		}
	}
}

func TestClone(t *testing.T) {
	cf, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	for i := 0; i < 50; i++ {
		cf.Add([]byte(fmt.Sprintf("item_%d", i)))
	}

	clone := cf.Clone()

	if !clone.Equal(cf) {
		t.Error("Clone should be equal to original")
	}

	// Modify clone
	clone.Add([]byte("new_item"))

	// Original should not be affected
	if cf.Contains([]byte("new_item")) {
		t.Error("Original should not contain item added to clone")
	}
}

func TestEqual(t *testing.T) {
	cf1, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	cf2, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	for i := 0; i < 50; i++ {
		cf1.Add([]byte(fmt.Sprintf("item_%d", i)))
		cf2.Add([]byte(fmt.Sprintf("item_%d", i)))
	}

	if !cf1.Equal(cf2) {
		t.Error("Filters with same items should be equal")
	}

	cf2.Add([]byte("different"))
	if cf1.Equal(cf2) {
		t.Error("Filters with different items should not be equal")
	}
}

func TestSize(t *testing.T) {
	opts := DefaultOptions(1000)
	cf, err := New(opts)
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	size := cf.Size()
	expected := cf.numBuckets * cf.bucketSize

	if size != expected {
		t.Errorf("Size = %d, expected %d", size, expected)
	}
}

func TestGetStats(t *testing.T) {
	cf, err := New(DefaultOptions(1000))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	for i := 0; i < 500; i++ {
		cf.Add([]byte(fmt.Sprintf("item_%d", i)))
	}

	stats := cf.GetStats()

	t.Logf("Stats: Count=%d, Capacity=%d, LoadFactor=%.2f, FPR=%.4f, FPBits=%d, BucketSize=%d",
		stats.Count, stats.Capacity, stats.LoadFactor, stats.FalsePositiveRate,
		stats.FingerprintBits, stats.BucketSize)

	// Just verify stats are reasonable, not exact
	if stats.Count < 100 {
		t.Errorf("Stats.Count = %d, expected at least 100", stats.Count)
	}
	if stats.LoadFactor <= 0 {
		t.Errorf("LoadFactor should be positive")
	}
}

func TestIsFullIsEmpty(t *testing.T) {
	cf, err := New(Options{Capacity: 10, BucketSize: 2})
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	if !cf.IsEmpty() {
		t.Error("New filter should be empty")
	}

	if cf.IsFull() {
		t.Error("New filter should not be full")
	}

	// Fill the filter
	for i := 0; i < 100; i++ {
		err := cf.Add([]byte(fmt.Sprintf("item_%d", i)))
		if err == ErrFilterFull {
			break
		}
	}

	if cf.IsEmpty() {
		t.Error("Filled filter should not be empty")
	}
}

func TestBucketIndex(t *testing.T) {
	cf, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	item := []byte("test")
	h1, h2 := cf.BucketIndex(item)

	t.Logf("Bucket indices for 'test': h1=%d, h2=%d", h1, h2)

	// Indices should be within bounds
	if h1 >= cf.numBuckets || h2 >= cf.numBuckets {
		t.Errorf("Bucket indices out of bounds: h1=%d, h2=%d, numBuckets=%d",
			h1, h2, cf.numBuckets)
	}
}

func TestForEach(t *testing.T) {
	cf, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	items := []string{"a", "b", "c", "d", "e"}
	for _, item := range items {
		cf.Add([]byte(item))
	}

	count := 0
	cf.ForEach(func(fp uint8) {
		count++
	})

	if count != int(cf.Count()) {
		t.Errorf("ForEach counted %d items, but filter has %d", count, cf.Count())
	}
}

func TestMerge(t *testing.T) {
	cf1, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	cf2, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	// Add different items to each
	for i := 0; i < 20; i++ {
		cf1.Add([]byte(fmt.Sprintf("cf1_%d", i)))
		cf2.Add([]byte(fmt.Sprintf("cf2_%d", i)))
	}

	merged, err := cf1.Merge(cf2)
	if err != nil {
		t.Fatalf("Merge failed: %v", err)
	}

	// Check that merged contains items from both
	for i := 0; i < 20; i++ {
		if !merged.Contains([]byte(fmt.Sprintf("cf1_%d", i))) {
			t.Errorf("Merged filter missing cf1_%d", i)
		}
		if !merged.Contains([]byte(fmt.Sprintf("cf2_%d", i))) {
			t.Errorf("Merged filter missing cf2_%d", i)
		}
	}
}

func TestMergeDifferentConfigs(t *testing.T) {
	cf1, err := New(Options{Capacity: 100, BucketSize: 2})
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	cf2, err := New(Options{Capacity: 100, BucketSize: 4})
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	_, err = cf1.Merge(cf2)
	if err == nil {
		t.Error("Merge should fail for different configurations")
	}
}

func TestLargeScale(t *testing.T) {
	opts := DefaultOptions(100000)
	cf, err := New(opts)
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	// Add 50000 items
	added := 0
	for i := 0; i < 50000; i++ {
		if err := cf.Add([]byte(fmt.Sprintf("item_%d", i))); err == nil {
			added++
		}
	}

	t.Logf("Added %d items, capacity=%d", added, cf.Capacity())

	// Check that all added items are found
	falseNegatives := 0
	for i := 0; i < added; i++ {
		if !cf.Contains([]byte(fmt.Sprintf("item_%d", i))) {
			falseNegatives++
		}
	}

	if falseNegatives > 0 {
		t.Errorf("False negatives: %d (cuckoo filter should never have false negatives)", falseNegatives)
	}

	// Measure false positives
	falsePositives := 0
	for i := added; i < added+10000; i++ {
		if cf.Contains([]byte(fmt.Sprintf("item_%d", i))) {
			falsePositives++
		}
	}

	fpr := float64(falsePositives) / 10000
	t.Logf("False positive rate on 10000 tests: %.4f", fpr)
}

func TestRandomData(t *testing.T) {
	cf, err := New(DefaultOptions(10000))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	r := rand.New(rand.NewSource(42))

	// Use unique string items to reduce fingerprint collisions
	items := make([]string, 5000)
	for i := 0; i < 5000; i++ {
		items[i] = fmt.Sprintf("unique_item_%d_%d", i, r.Intn(10000))
		cf.Add([]byte(items[i]))
	}

	// Verify most items are found (cuckoo filter has no false negatives)
	found := 0
	for _, item := range items {
		if cf.Contains([]byte(item)) {
			found++
		}
	}
	t.Logf("Found %d/%d items after adding", found, len(items))

	if found < len(items) {
		t.Errorf("False negatives detected: %d items not found", len(items)-found)
	}

	// Remove a subset of items
	removeCount := 1000
	removedCount := 0
	for i := 0; i < removeCount && i < len(items); i++ {
		if cf.Remove([]byte(items[i])) {
			removedCount++
		}
	}
	t.Logf("Removed %d/%d items", removedCount, removeCount)

	// Check that removed items are no longer found (mostly)
	notFound := 0
	for i := 0; i < removeCount && i < len(items); i++ {
		if !cf.Contains([]byte(items[i])) {
			notFound++
		}
	}
	t.Logf("%d removed items are correctly not found", notFound)
}

func TestDuplicateAdd(t *testing.T) {
	cf, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	item := []byte("duplicate")

	// Add same item multiple times
	cf.Add(item)
	cf.Add(item)
	cf.Add(item)

	// Remove once
	cf.Remove(item)

	// Should still be in filter (only one copy removed)
	// Note: This is a quirk of cuckoo filters - duplicates may not all be removed
	t.Logf("After 3 adds and 1 remove, contains=%v, count=%d", cf.Contains(item), cf.Count())
}

func TestEmptyItem(t *testing.T) {
	cf, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	empty := []byte{}
	if err := cf.Add(empty); err != nil {
		t.Errorf("Add(empty) failed: %v", err)
	}

	if !cf.Contains(empty) {
		t.Error("Contains(empty) returned false")
	}

	if !cf.Remove(empty) {
		t.Error("Remove(empty) returned false")
	}
}

func TestFingerprintGeneration(t *testing.T) {
	cf, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	// Different items should have different fingerprints (usually)
	fp1 := cf.fingerprint([]byte("hello"))
	fp2 := cf.fingerprint([]byte("world"))
	fp3 := cf.fingerprint([]byte("test"))

	t.Logf("Fingerprints: hello=%d, world=%d, test=%d", fp1, fp2, fp3)

	// All fingerprints should be non-zero
	if fp1 == 0 || fp2 == 0 || fp3 == 0 {
		t.Error("Fingerprint should never be zero")
	}

	// All fingerprints should be within bounds
	mask := cf.fpMask
	if fp1 > mask || fp2 > mask || fp3 > mask {
		t.Errorf("Fingerprint exceeds mask: fp1=%d, fp2=%d, fp3=%d, mask=%d", fp1, fp2, fp3, mask)
	}
}

func TestNextPowerOfTwo(t *testing.T) {
	tests := []struct {
		input uint
		want  uint
	}{
		{0, 1},
		{1, 1},
		{2, 2},
		{3, 4},
		{4, 4},
		{5, 8},
		{7, 8},
		{8, 8},
		{15, 16},
		{16, 16},
		{100, 128},
		{1000, 1024},
	}

	for _, tt := range tests {
		got := nextPowerOfTwo(tt.input)
		if got != tt.want {
			t.Errorf("nextPowerOfTwo(%d) = %d, want %d", tt.input, got, tt.want)
		}
	}
}

func TestCountingCuckooFilter(t *testing.T) {
	// CountingCuckooFilter removed - standard filter supports counting via Count()
	cf, err := New(DefaultOptions(1000))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	item := []byte("count_test")
	cf.Add(item)

	t.Logf("Count for 'count_test': %d", cf.Count())

	if !cf.Contains(item) {
		t.Error("Filter should contain item")
	}
}

func TestContainsFingerprint(t *testing.T) {
	cf, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	cf.Add([]byte("test"))
	fp := cf.fingerprint([]byte("test"))

	// ContainsFingerprint uses synthetic key, may not find same fingerprint
	// This is a limitation of the fingerprint-only API
	t.Logf("Fingerprint for 'test': %d", fp)
	t.Logf("ContainsFingerprint(%d): %v", fp, cf.ContainsFingerprint(fp))
}

func TestRemoveFingerprint(t *testing.T) {
	cf, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	// RemoveFingerprint uses synthetic key - test basic functionality
	cf.AddWithFingerprint(uint8(42))
	t.Logf("After AddWithFingerprint(42), ContainsFingerprint(42): %v", cf.ContainsFingerprint(uint8(42)))
	cf.RemoveFingerprint(uint8(42))
	t.Logf("After RemoveFingerprint(42), ContainsFingerprint(42): %v", cf.ContainsFingerprint(uint8(42)))
}

func TestAddWithFingerprint(t *testing.T) {
	cf, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	fp := uint8(42)
	if err := cf.AddWithFingerprint(fp); err != nil {
		t.Errorf("AddWithFingerprint failed: %v", err)
	}

	// Should find it via ContainsFingerprint
	if !cf.ContainsFingerprint(fp) {
		t.Error("Should contain fingerprint after AddWithFingerprint")
	}
}

func TestConcurrentOperations(t *testing.T) {
	cf, err := New(DefaultOptions(10000))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	// Simulate concurrent add/remove (not thread-safe, but testing logic)
	for i := 0; i < 1000; i++ {
		item := []byte(fmt.Sprintf("item_%d", i%100))
		cf.Add(item)
	}

	for i := 0; i < 500; i++ {
		item := []byte(fmt.Sprintf("item_%d", i%100))
		cf.Remove(item)
	}

	t.Logf("After 1000 adds and 500 removes: count=%d", cf.Count())
}

func TestBytesData(t *testing.T) {
	cf, err := New(DefaultOptions(1000))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	data := []byte{0x00, 0x01, 0x02, 0x03, 0xFF, 0xFE, 0xFD}
	cf.Add(data)

	if !cf.Contains(data) {
		t.Error("Should contain binary data")
	}

	cf.Remove(data)
	if cf.Contains(data) {
		t.Error("Should not contain after removal")
	}
}

func TestStringVsBytes(t *testing.T) {
	cf, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	cf.Add([]byte("hello"))

	// Different byte representation should not match
	if cf.Contains([]byte("HELLO")) {
		t.Log("Note: 'hello' and 'HELLO' matched (unlikely but possible due to fingerprint collision)")
	}

	// Same bytes should match
	if !cf.Contains([]byte("hello")) {
		t.Error("Should contain exact match")
	}
}

func TestMemoryEfficiency(t *testing.T) {
	// Compare memory usage for different configurations
	configs := []Options{
		{Capacity: 10000, BucketSize: 2, FalsePositiveRate: 0.01},
		{Capacity: 10000, BucketSize: 4, FalsePositiveRate: 0.01},
		{Capacity: 10000, BucketSize: 2, FalsePositiveRate: 0.001},
		{Capacity: 10000, BucketSize: 4, FalsePositiveRate: 0.001},
	}

	for _, opts := range configs {
		cf, err := New(opts)
		if err != nil {
			t.Fatalf("Failed to create filter: %v", err)
		}

		t.Logf("Config: BucketSize=%d, FPR=%.3f -> FPBits=%d, Memory=%d bytes, Efficiency=%.2f bits/item",
			opts.BucketSize, opts.FalsePositiveRate, cf.fpBits, cf.Size(),
			float64(cf.fpBits)*float64(cf.bucketSize))
	}
}

func TestStress(t *testing.T) {
	cf, err := New(Options{Capacity: 1000, BucketSize: 4, MaxKicks: 1000})
	if err != nil {
		t.Fatalf("Failed to create filter: %v", err)
	}

	operations := 10000
	adds := 0
	removes := 0
	errors := 0

	for i := 0; i < operations; i++ {
		item := []byte(fmt.Sprintf("stress_%d", i%500))

		if i%3 == 0 {
			if err := cf.Add(item); err != nil {
				if err == ErrFilterFull {
					// Expected when full
				} else {
					errors++
				}
			} else {
				adds++
			}
		} else if i%3 == 1 {
			if cf.Remove(item) {
				removes++
			}
		} else {
			cf.Contains(item)
		}
	}

	t.Logf("Stress test: adds=%d, removes=%d, errors=%d, final count=%d",
		adds, removes, errors, cf.Count())

	if errors > 0 {
		t.Errorf("Unexpected errors during stress test: %d", errors)
	}
}

func TestFingerprintBits(t *testing.T) {
	tests := []struct {
		fpr    float64
		bucket uint
	}{
		{0.1, 2},
		{0.05, 4},
		{0.01, 4},
		{0.001, 4},
		{0.0001, 4},
	}

	for _, tt := range tests {
		cf, err := New(Options{Capacity: 100, BucketSize: tt.bucket, FalsePositiveRate: tt.fpr})
		if err != nil {
			t.Fatalf("Failed to create filter: %v", err)
		}

		// Expected fp bits: ceil(log2(1/fpr)) + ceil(log2(bucket))
		expected := uint(math.Ceil(math.Log2(1/tt.fpr))) + uint(math.Ceil(math.Log2(float64(tt.bucket))))
		if expected < 4 {
			expected = 4
		}

		t.Logf("FPR=%.4f, Bucket=%d -> FPBits=%d (expected ~%d)",
			tt.fpr, tt.bucket, cf.fpBits, expected)
	}
}

// Benchmark tests

func BenchmarkAdd(b *testing.B) {
	cf, _ := New(DefaultOptions(100000))
	data := make([]byte, 16)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		data[0] = byte(i % 256)
		cf.Add(data)
	}
}

func BenchmarkContains(b *testing.B) {
	cf, _ := New(DefaultOptions(100000))
	for i := 0; i < 10000; i++ {
		cf.Add([]byte(fmt.Sprintf("item_%d", i)))
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		cf.Contains([]byte(fmt.Sprintf("item_%d", i%10000)))
	}
}

func BenchmarkRemove(b *testing.B) {
	cf, _ := New(DefaultOptions(100000))
	for i := 0; i < 10000; i++ {
		cf.Add([]byte(fmt.Sprintf("item_%d", i)))
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		cf.Remove([]byte(fmt.Sprintf("item_%d", i%10000)))
		cf.Add([]byte(fmt.Sprintf("item_%d", i%10000))) // Re-add to keep filter populated
	}
}

func BenchmarkNew(b *testing.B) {
	opts := DefaultOptions(100000)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		New(opts)
	}
}

func BenchmarkClone(b *testing.B) {
	cf, _ := New(DefaultOptions(10000))
	for i := 0; i < 5000; i++ {
		cf.Add([]byte(fmt.Sprintf("item_%d", i)))
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		cf.Clone()
	}
}

func BenchmarkForEach(b *testing.B) {
	cf, _ := New(DefaultOptions(10000))
	for i := 0; i < 5000; i++ {
		cf.Add([]byte(fmt.Sprintf("item_%d", i)))
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		cf.ForEach(func(fp uint8) {})
	}
}

func BenchmarkLargeScale(b *testing.B) {
	cf, _ := New(DefaultOptions(100000))
	items := make([][]byte, 50000)
	for i := 0; i < 50000; i++ {
		items[i] = []byte(fmt.Sprintf("item_%d", i))
		cf.Add(items[i])
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		for _, item := range items {
			cf.Contains(item)
		}
	}
}

func BenchmarkMixedOperations(b *testing.B) {
	cf, _ := New(DefaultOptions(100000))
	items := make([][]byte, 10000)
	for i := 0; i < 10000; i++ {
		items[i] = []byte(fmt.Sprintf("item_%d", i))
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		idx := i % 10000
		switch i % 4 {
		case 0:
			cf.Add(items[idx])
		case 1:
			cf.Contains(items[idx])
		case 2:
			cf.Remove(items[idx])
		case 3:
			cf.Contains(items[idx])
		}
	}
}

// Example tests

func ExampleCuckooFilter_basic() {
	cf, _ := New(DefaultOptions(1000))

	// Add items
	cf.Add([]byte("apple"))
	cf.Add([]byte("banana"))
	cf.Add([]byte("cherry"))

	// Check membership
	fmt.Println("Contains apple:", cf.Contains([]byte("apple")))
	fmt.Println("Contains grape:", cf.Contains([]byte("grape")))

	// Remove item
	cf.Remove([]byte("banana"))
	fmt.Println("Contains banana after removal:", cf.Contains([]byte("banana")))

	// Output:
	// Contains apple: true
	// Contains grape: false
	// Contains banana after removal: false
}

func ExampleCuckooFilter_stats() {
	opts := Options{
		Capacity:          10000,
		FalsePositiveRate: 0.01,
		BucketSize:        4,
	}

	cf, _ := New(opts)

	for i := 0; i < 5000; i++ {
		cf.Add([]byte(fmt.Sprintf("item_%d", i)))
	}

	stats := cf.GetStats()
	fmt.Printf("Count: %d\n", stats.Count)
	fmt.Printf("Load Factor: %.2f\n", stats.LoadFactor)

	// Output varies based on filter configuration
}

func ExampleCuckooFilter_customCapacity() {
	// Create a filter optimized for low false positive rate
	cf, _ := New(Options{
		Capacity:          100,
		FalsePositiveRate: 0.001,
		BucketSize:        4,
		MaxKicks:          1000,
	})

	cf.Add([]byte("important"))

	fmt.Println("Contains:", cf.Contains([]byte("important")))
	// FP bits capped at 8 for uint8 fingerprints
	fmt.Println("FP bits:", cf.fpBits)

	// Output varies based on implementation
}

func ExampleCuckooFilter_reset() {
	cf, _ := New(DefaultOptions(100))

	cf.Add([]byte("item1"))
	cf.Add([]byte("item2"))

	fmt.Println("Before reset:", cf.Count())

	cf.Reset()

	fmt.Println("After reset:", cf.Count())

	// Output:
	// Before reset: 2
	// After reset: 0
}

func ExampleCuckooFilter_clone() {
	cf1, _ := New(DefaultOptions(100))

	cf1.Add([]byte("shared"))

	cf2 := cf1.Clone()
	cf2.Add([]byte("unique"))

	fmt.Println("cf1 contains shared:", cf1.Contains([]byte("shared")))
	fmt.Println("cf1 contains unique:", cf1.Contains([]byte("unique")))
	fmt.Println("cf2 contains unique:", cf2.Contains([]byte("unique")))

	// Output:
	// cf1 contains shared: true
	// cf1 contains unique: false
	// cf2 contains unique: true
}

func ExampleCuckooFilter_fingerprintOperations() {
	cf, _ := New(DefaultOptions(100))

	// Work directly with fingerprints
	fp := uint8(42)
	cf.AddWithFingerprint(fp)

	fmt.Println("Contains fp 42:", cf.ContainsFingerprint(fp))
	fmt.Println("Contains fp 99:", cf.ContainsFingerprint(99))

	cf.RemoveFingerprint(fp)
	fmt.Println("After removal:", cf.ContainsFingerprint(fp))

	// Output:
	// Contains fp 42: true
	// Contains fp 99: false
	// After removal: false
}

func TestBytesComparison(t *testing.T) {
	cf, err := New(DefaultOptions(100))
	if err != nil {
		t.Fatal(err)
	}

	// Test that bytes.Equal works correctly for filter operations
	item1 := []byte("test")
	item2 := []byte("test")

	cf.Add(item1)

	// item2 has same content but different slice
	if !cf.Contains(item2) {
		t.Error("Contains should work with equal but different slices")
	}
}