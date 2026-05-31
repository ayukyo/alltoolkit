package autocomplete

import (
	"fmt"
	"testing"
)

func TestNewTrie(t *testing.T) {
	trie := New()
	if trie == nil {
		t.Fatal("New() returned nil")
	}
	if trie.totalWords != 0 {
		t.Errorf("Expected 0 total words, got %d", trie.totalWords)
	}
}

func TestNewTrieCaseInsensitive(t *testing.T) {
	trie := NewCaseInsensitive()
	if trie == nil {
		t.Fatal("NewCaseInsensitive() returned nil")
	}
	if trie.caseSensitive {
		t.Error("Expected case insensitive mode")
	}
}

func TestInsert(t *testing.T) {
	trie := New()
	trie.Insert("hello")
	trie.Insert("world")
	trie.Insert("help")
	trie.Insert("helicopter")

	if trie.totalWords != 4 {
		t.Errorf("Expected 4 total words, got %d", trie.totalWords)
	}
}

func TestInsertBatch(t *testing.T) {
	trie := New()
	words := []string{"apple", "banana", "apricot", "blueberry", "cherry"}
	trie.InsertBatch(words)

	if trie.totalWords != 5 {
		t.Errorf("Expected 5 total words, got %d", trie.totalWords)
	}
}

func TestContains(t *testing.T) {
	trie := New()
	trie.Insert("hello")
	trie.Insert("world")

	if !trie.Contains("hello") {
		t.Error("Contains(hello) returned false, expected true")
	}
	if !trie.Contains("world") {
		t.Error("Contains(world) returned false, expected true")
	}
	if trie.Contains("missing") {
		t.Error("Contains(missing) returned true, expected false")
	}
}

func TestContainsCaseInsensitive(t *testing.T) {
	trie := NewCaseInsensitive()
	trie.Insert("Hello")
	trie.Insert("WORLD")

	if !trie.Contains("hello") {
		t.Error("Contains(hello) returned false, expected true")
	}
	if !trie.Contains("World") {
		t.Error("Contains(World) returned false, expected true")
	}
	if !trie.Contains("HELLO") {
		t.Error("Contains(HELLO) returned false, expected true")
	}
}

func TestComplete(t *testing.T) {
	trie := New()
	words := []string{
		"hello",
		"help",
		"helicopter",
		"world",
		"works",
		"working",
	}
	trie.InsertBatch(words)

	suggestions := trie.Complete("hel", 10)
	if len(suggestions) != 3 {
		t.Errorf("Expected 3 suggestions, got %d: %v", len(suggestions), suggestions)
	}
}

func TestCompleteWithLimit(t *testing.T) {
	trie := New()
	words := []string{"apple", "apricot", "banana", "blueberry", "cherry"}
	trie.InsertBatch(words)

	suggestions := trie.Complete("a", 2)
	if len(suggestions) != 2 {
		t.Errorf("Expected 2 suggestions, got %d", len(suggestions))
	}
}

func TestCompleteEmptyPrefix(t *testing.T) {
	trie := New()
	trie.Insert("hello")
	trie.Insert("world")

	suggestions := trie.Complete("", 10)
	if len(suggestions) != 2 {
		t.Errorf("Expected 2 suggestions for empty prefix, got %d", len(suggestions))
	}
}

func TestCompleteNoMatch(t *testing.T) {
	trie := New()
	trie.Insert("hello")
	trie.Insert("world")

	suggestions := trie.Complete("xyz", 10)
	if len(suggestions) != 0 {
		t.Errorf("Expected 0 suggestions, got %d", len(suggestions))
	}
}

func TestCompleteSortedByFrequency(t *testing.T) {
	trie := New()
	// Insert "help" more frequently
	trie.Insert("help")
	trie.Insert("hello")
	trie.Insert("help")
	trie.Insert("help")

	suggestions := trie.Complete("he", 10)
	if len(suggestions) < 2 {
		t.Fatalf("Expected at least 2 suggestions, got %d", len(suggestions))
	}

	// "help" should be first because it has the highest frequency
	if suggestions[0] != "help" {
		t.Errorf("Expected 'help' to be first suggestion, got '%s'", suggestions[0])
	}
}

func TestPrefixExists(t *testing.T) {
	trie := New()
	trie.Insert("hello")
	trie.Insert("world")

	if !trie.PrefixExists("hel") {
		t.Error("PrefixExists(hel) returned false, expected true")
	}
	if !trie.PrefixExists("wor") {
		t.Error("PrefixExists(wor) returned false, expected true")
	}
	if trie.PrefixExists("xyz") {
		t.Error("PrefixExists(xyz) returned true, expected false")
	}
}

func TestRemove(t *testing.T) {
	trie := New()
	trie.Insert("hello")
	trie.Insert("world")

	if !trie.Remove("hello") {
		t.Error("Remove(hello) returned false, expected true")
	}
	if trie.totalWords != 1 {
		t.Errorf("Expected 1 total word, got %d", trie.totalWords)
	}
	if trie.Contains("hello") {
		t.Error("Contains(hello) returned true after removal")
	}
	if !trie.Contains("world") {
		t.Error("Contains(world) returned false, expected true")
	}
}

func TestRemoveNonExistent(t *testing.T) {
	trie := New()
	trie.Insert("hello")

	if trie.Remove("world") {
		t.Error("Remove(world) returned true, expected false")
	}
}

func TestWordCount(t *testing.T) {
	trie := New()
	if trie.WordCount() != 0 {
		t.Errorf("Expected 0 words, got %d", trie.WordCount())
	}

	trie.Insert("hello")
	trie.Insert("world")
	if trie.WordCount() != 2 {
		t.Errorf("Expected 2 words, got %d", trie.WordCount())
	}

	// Inserting duplicate should not increase count
	trie.Insert("hello")
	if trie.WordCount() != 2 {
		t.Errorf("Expected 2 words after duplicate insert, got %d", trie.WordCount())
	}
}

func TestClear(t *testing.T) {
	trie := New()
	trie.Insert("hello")
	trie.Insert("world")
	trie.Clear()

	if trie.totalWords != 0 {
		t.Errorf("Expected 0 total words after clear, got %d", trie.totalWords)
	}
	if trie.Contains("hello") {
		t.Error("Contains(hello) returned true after clear")
	}
}

func TestGetFrequency(t *testing.T) {
	trie := New()
	trie.Insert("hello")
	trie.Insert("world")
	trie.Insert("hello")

	if trie.GetFrequency("hello") != 2 {
		t.Errorf("Expected frequency 2 for hello, got %d", trie.GetFrequency("hello"))
	}
	if trie.GetFrequency("world") != 1 {
		t.Errorf("Expected frequency 1 for world, got %d", trie.GetFrequency("world"))
	}
	if trie.GetFrequency("missing") != 0 {
		t.Errorf("Expected frequency 0 for missing, got %d", trie.GetFrequency("missing"))
	}
}

func TestCompleteWithDetails(t *testing.T) {
	trie := New()
	trie.Insert("hello")
	trie.Insert("world")
	trie.Insert("hello") // hello has frequency 2

	details := trie.CompleteWithDetails("he", 10)
	if len(details) != 1 {
		t.Fatalf("Expected 1 detail, got %d", len(details))
	}
	if details[0].Word != "hello" {
		t.Errorf("Expected word 'hello', got '%s'", details[0].Word)
	}
	if details[0].Frequency != 2 {
		t.Errorf("Expected frequency 2, got %d", details[0].Frequency)
	}
}

func TestEmptyTrieComplete(t *testing.T) {
	trie := New()
	suggestions := trie.Complete("anything", 10)
	if len(suggestions) != 0 {
		t.Errorf("Expected 0 suggestions from empty trie, got %d", len(suggestions))
	}
}

func TestSingleCharPrefix(t *testing.T) {
	trie := New()
	trie.Insert("a")
	trie.Insert("ab")
	trie.Insert("abc")
	trie.Insert("abd")
	trie.Insert("b")
	trie.Insert("bc")

	suggestions := trie.Complete("a", 10)
	if len(suggestions) != 4 {
		t.Errorf("Expected 4 suggestions, got %d: %v", len(suggestions), suggestions)
	}
}

func TestUnicodeSupport(t *testing.T) {
	trie := New()
	trie.Insert("你好")
	trie.Insert("世界")
	trie.Insert("你好吗")

	suggestions := trie.Complete("你", 10)
	if len(suggestions) != 2 {
		t.Errorf("Expected 2 suggestions, got %d: %v", len(suggestions), suggestions)
	}
}

func TestCompleteCaseInsensitive(t *testing.T) {
	trie := NewCaseInsensitive()
	trie.Insert("Hello")
	trie.Insert("Help")
	trie.Insert("World")

	suggestions := trie.Complete("HE", 10)
	if len(suggestions) != 2 {
		t.Errorf("Expected 2 suggestions, got %d: %v", len(suggestions), suggestions)
	}
}

func TestExample(t *testing.T) {
	// Build a dictionary
	dictionary := []string{
		"apple", "apricot", "banana", "blueberry", "cherry",
		"grape", "grapefruit", "kiwi", "lemon", "lime",
		"mango", "melon", "orange", "papaya", "peach",
		"pear", "plum", "pomegranate", "raspberry", "strawberry",
		"watermelon",
	}

	trie := New()
	trie.InsertBatch(dictionary)

	// Test autocomplete
	suggestions := trie.Complete("gr", 10)
	expected := []string{"grape", "grapefruit"}
	if len(suggestions) != len(expected) {
		t.Errorf("Expected %v, got %v", expected, suggestions)
	}
}

func BenchmarkInsert(b *testing.B) {
	trie := New()
	words := []string{"apple", "banana", "cherry", "date", "elderberry", "fig", "grape"}
	for i := 0; i < b.N; i++ {
		trie.Insert(words[i%len(words)])
	}
}

func BenchmarkComplete(b *testing.B) {
	trie := New()
	dictionary := []string{
		"apple", "apricot", "banana", "blueberry", "cherry",
		"grape", "grapefruit", "kiwi", "lemon", "lime",
		"mango", "melon", "orange", "papaya", "peach",
	}
	trie.InsertBatch(dictionary)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		trie.Complete("gr", 10)
	}
}

func Example() {
	trie := New()

	// Build dictionary
	dictionary := []string{
		"hello",
		"world",
		"help",
		"helicopter",
		"hero",
		"heroine",
		"work",
		"working",
		"works",
		"workshop",
	}
	trie.InsertBatch(dictionary)

	// Get suggestions
	allSuggestions := trie.Complete("", 10)
	fmt.Printf("Total words in dictionary: %d\n", len(allSuggestions))

	// Output:
	// Total words in dictionary: 10
}

func ExampleNewCaseInsensitive() {
	trie := NewCaseInsensitive()

	trie.Insert("Hello")
	trie.Insert("HELLO")
	trie.Insert("World")

	fmt.Printf("Contains 'hello': %v\n", trie.Contains("hello"))
	fmt.Printf("Word count: %d\n", trie.WordCount())
	fmt.Printf("Frequency of 'hello': %d\n", trie.GetFrequency("hello"))

	// Output:
	// Contains 'hello': true
	// Word count: 2
	// Frequency of 'hello': 2
}