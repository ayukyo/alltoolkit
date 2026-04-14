package bloom_filter

import (
	"testing"
)

func TestNew(t *testing.T) {
	bf := New(1000, 5)
	if bf.Size() != 1000 {
		t.Errorf("Expected size 1000, got %d", bf.Size())
	}
	if bf.HashCount() != 5 {
		t.Errorf("Expected hash count 5, got %d", bf.HashCount())
	}
	if bf.Count() != 0 {
		t.Errorf("Expected count 0, got %d", bf.Count())
	}
}

func TestNewWithConfig(t *testing.T) {
	tests := []struct {
		name          string
		expectedItems uint
		fpRate        float64
	}{
		{"default values", 0, 0},
		{"small", 100, 0.01},
		{"medium", 10000, 0.001},
		{"large", 1000000, 0.0001},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			config := Config{
				ExpectedItems:     tt.expectedItems,
				FalsePositiveRate: tt.fpRate,
			}
			bf := NewWithConfig(config)
			if bf == nil {
				t.Fatal("Expected non-nil Bloom filter")
			}
			if bf.Size() == 0 {
				t.Error("Expected non-zero size")
			}
			if bf.HashCount() == 0 {
				t.Error("Expected non-zero hash count")
			}
		})
	}
}

func TestNewDefault(t *testing.T) {
	bf := NewDefault()
	if bf == nil {
		t.Fatal("Expected non-nil Bloom filter")
	}
	if bf.Size() == 0 {
		t.Error("Expected non-zero size")
	}
}

func TestAddAndContains(t *testing.T) {
	bf := New(10000, 7)

	// Test with bytes
	data := []byte("test-data")
	bf.Add(data)

	if !bf.Contains(data) {
		t.Error("Expected to find added item")
	}

	// Test non-existent item
	if bf.Contains([]byte("non-existent")) {
		t.Error("Did not expect to find non-existent item")
	}
}

func TestAddAndContainsString(t *testing.T) {
	bf := New(10000, 7)

	testStrings := []string{"hello", "world", "foo", "bar", "bloom", "filter"}
	for _, s := range testStrings {
		bf.AddString(s)
	}

	// All added strings should be found
	for _, s := range testStrings {
		if !bf.ContainsString(s) {
			t.Errorf("Expected to find string: %s", s)
		}
	}

	// Non-existent strings should not be found
	if bf.ContainsString("not-added") {
		t.Error("Did not expect to find non-existent string")
	}
}

func TestClear(t *testing.T) {
	bf := New(1000, 5)

	bf.AddString("test1")
	bf.AddString("test2")
	bf.AddString("test3")

	if bf.Count() != 3 {
		t.Errorf("Expected count 3, got %d", bf.Count())
	}

	bf.Clear()

	if bf.Count() != 0 {
		t.Errorf("Expected count 0 after clear, got %d", bf.Count())
	}

	if bf.ContainsString("test1") {
		t.Error("Did not expect to find item after clear")
	}
}

func TestFillRatio(t *testing.T) {
	bf := New(100, 3)

	if bf.FillRatio() != 0 {
		t.Error("Expected fill ratio 0 for empty filter")
	}

	// Add some items
	for i := 0; i < 10; i++ {
		bf.AddString(string(rune('a' + i)))
	}

	if bf.FillRatio() <= 0 || bf.FillRatio() > 1 {
		t.Errorf("Fill ratio should be between 0 and 1, got %f", bf.FillRatio())
	}
}

func TestFalsePositiveRate(t *testing.T) {
	bf := NewWithConfig(Config{
		ExpectedItems:     1000,
		FalsePositiveRate: 0.01,
	})

	// Empty filter should have near-zero FP rate
	if bf.FalsePositiveRate() > 0.01 {
		t.Errorf("Expected low FP rate for empty filter, got %f", bf.FalsePositiveRate())
	}

	// Add items up to expected capacity
	for i := 0; i < 1000; i++ {
		bf.AddString(string(rune(i)))
	}

	// FP rate should be around the expected rate
	fpRate := bf.FalsePositiveRate()
	if fpRate > 0.1 { // Allow some margin
		t.Errorf("FP rate too high: %f", fpRate)
	}
}

func TestStats(t *testing.T) {
	bf := NewWithConfig(Config{
		ExpectedItems:     100,
		FalsePositiveRate: 0.01,
	})

	for i := 0; i < 50; i++ {
		bf.AddString(string(rune(i)))
	}

	stats := bf.Stats()

	if stats.Size != bf.Size() {
		t.Errorf("Stats size mismatch")
	}
	if stats.HashCount != bf.HashCount() {
		t.Errorf("Stats hash count mismatch")
	}
	if stats.ItemCount != 50 {
		t.Errorf("Expected item count 50, got %d", stats.ItemCount)
	}
	if stats.FillRatio <= 0 {
		t.Error("Expected non-zero fill ratio")
	}
}

func TestExportImport(t *testing.T) {
	original := NewWithConfig(Config{
		ExpectedItems:     1000,
		FalsePositiveRate: 0.01,
	})

	// Add some items
	testItems := []string{"apple", "banana", "cherry", "date", "elderberry"}
	for _, item := range testItems {
		original.AddString(item)
	}

	// Export
	exported := original.Export()
	if exported.Size != original.Size() {
		t.Error("Exported size mismatch")
	}
	if exported.Count != original.Count() {
		t.Error("Exported count mismatch")
	}

	// Import
	imported, err := Import(exported)
	if err != nil {
		t.Fatalf("Import failed: %v", err)
	}

	// Verify imported filter has same properties
	if imported.Size() != original.Size() {
		t.Error("Imported size mismatch")
	}
	if imported.HashCount() != original.HashCount() {
		t.Error("Imported hash count mismatch")
	}

	// Verify all items can still be found
	for _, item := range testItems {
		if !imported.ContainsString(item) {
			t.Errorf("Imported filter doesn't contain: %s", item)
		}
	}
}

func TestToFromJSON(t *testing.T) {
	original := NewWithConfig(Config{
		ExpectedItems:     1000,
		FalsePositiveRate: 0.01,
	})

	testItems := []string{"foo", "bar", "baz"}
	for _, item := range testItems {
		original.AddString(item)
	}

	// To JSON
	jsonStr, err := original.ToJSON()
	if err != nil {
		t.Fatalf("ToJSON failed: %v", err)
	}
	if jsonStr == "" {
		t.Error("Expected non-empty JSON string")
	}

	// From JSON
	imported, err := FromJSON(jsonStr)
	if err != nil {
		t.Fatalf("FromJSON failed: %v", err)
	}

	// Verify items
	for _, item := range testItems {
		if !imported.ContainsString(item) {
			t.Errorf("Imported filter doesn't contain: %s", item)
		}
	}
}

func TestUnion(t *testing.T) {
	bf1 := New(1000, 5)
	bf2 := New(1000, 5)

	bf1.AddString("apple")
	bf1.AddString("banana")

	bf2.AddString("cherry")
	bf2.AddString("date")

	union, err := bf1.Union(bf2)
	if err != nil {
		t.Fatalf("Union failed: %v", err)
	}

	// Union should contain all items from both filters
	if !union.ContainsString("apple") {
		t.Error("Union should contain 'apple'")
	}
	if !union.ContainsString("banana") {
		t.Error("Union should contain 'banana'")
	}
	if !union.ContainsString("cherry") {
		t.Error("Union should contain 'cherry'")
	}
	if !union.ContainsString("date") {
		t.Error("Union should contain 'date'")
	}
}

func TestUnionDifferentSizes(t *testing.T) {
	bf1 := New(1000, 5)
	bf2 := New(2000, 5)

	_, err := bf1.Union(bf2)
	if err == nil {
		t.Error("Expected error for different sized filters")
	}
}

func TestIntersect(t *testing.T) {
	bf1 := New(1000, 5)
	bf2 := New(1000, 5)

	bf1.AddString("apple")
	bf1.AddString("banana")
	bf1.AddString("cherry")

	bf2.AddString("banana")
	bf2.AddString("cherry")
	bf2.AddString("date")

	intersect, err := bf1.Intersect(bf2)
	if err != nil {
		t.Fatalf("Intersect failed: %v", err)
	}

	// Intersection should contain items that are in both
	if !intersect.ContainsString("banana") {
		t.Error("Intersection should contain 'banana'")
	}
	if !intersect.ContainsString("cherry") {
		t.Error("Intersection should contain 'cherry'")
	}
}

func TestIntersectDifferentSizes(t *testing.T) {
	bf1 := New(1000, 5)
	bf2 := New(1000, 7) // Different hash count

	_, err := bf1.Intersect(bf2)
	if err == nil {
		t.Error("Expected error for different hash count filters")
	}
}

func TestString(t *testing.T) {
	bf := New(1000, 5)
	bf.AddString("test")

	str := bf.String()
	if str == "" {
		t.Error("Expected non-empty string representation")
	}
}

func TestImportNil(t *testing.T) {
	_, err := Import(nil)
	if err == nil {
		t.Error("Expected error for nil export")
	}
}

func TestFromJSONInvalid(t *testing.T) {
	_, err := FromJSON("invalid json")
	if err == nil {
		t.Error("Expected error for invalid JSON")
	}
}

func TestFromJSONInvalidBase64(t *testing.T) {
	jsonStr := `{"size":100,"hash_count":5,"count":1,"bitmap":"!!invalid-base64!!"}`
	_, err := FromJSON(jsonStr)
	if err == nil {
		t.Error("Expected error for invalid base64")
	}
}

func BenchmarkAdd(b *testing.B) {
	bf := New(uint(b.N*10), 7)
	data := []byte("benchmark-data")
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		bf.Add(data)
	}
}

func BenchmarkContains(b *testing.B) {
	bf := New(100000, 7)
	bf.AddString("benchmark-item")
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		bf.ContainsString("benchmark-item")
	}
}

func BenchmarkAddString(b *testing.B) {
	bf := New(uint(b.N*10), 7)
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		bf.AddString("benchmark-string")
	}
}

func BenchmarkToJSON(b *testing.B) {
	bf := NewWithConfig(Config{
		ExpectedItems:     10000,
		FalsePositiveRate: 0.01,
	})
	for i := 0; i < 5000; i++ {
		bf.AddString(string(rune(i)))
	}
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = bf.ToJSON()
	}
}

func BenchmarkFromJSON(b *testing.B) {
	bf := NewWithConfig(Config{
		ExpectedItems:     10000,
		FalsePositiveRate: 0.01,
	})
	for i := 0; i < 5000; i++ {
		bf.AddString(string(rune(i)))
	}
	jsonStr, _ := bf.ToJSON()
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = FromJSON(jsonStr)
	}
}