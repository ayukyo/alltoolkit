package memoize_utils

import (
	"fmt"
	"time"
)

// ============================================================================
// Basic Usage Examples
// ============================================================================

func ExampleLRUCache_basic() {
	// Create a cache with max size of 100 entries
	cache := NewLRUCache[string, string](WithMaxSize(100))

	// Set values
	cache.Set("user:1", "Alice")
	cache.Set("user:2", "Bob")

	// Get values
	if name, ok := cache.Get("user:1"); ok {
		fmt.Println(name)
	}

	// Check if key exists
	fmt.Println(cache.Has("user:2"))
	fmt.Println(cache.Has("user:3"))

	// Get cache size
	fmt.Printf("Cache size: %d\n", cache.Size())

	// Output:
	// Alice
	// true
	// false
	// Cache size: 2
}

func ExampleLRUCache_withTTL() {
	// Create a cache with 5-minute TTL
	cache := NewLRUCache[string, string](
		WithMaxSize(100),
		WithTTL(5*time.Minute),
	)

	cache.Set("session:abc", "user123")

	// Check remaining TTL
	if elem, ok := cache.items["session:abc"]; ok {
		entry := elem.Value.(*lruEntry[string, string]).entry
		ttl := entry.TTL()
		fmt.Printf("TTL remaining: %v seconds\n", ttl.Seconds())
	}
}

func ExampleLRUCache_getOrCompute() {
	cache := NewLRUCache[string, int](WithMaxSize(100))

	// Expensive computation function
	computeScore := func() (int, error) {
		// Simulate expensive calculation
		return 42, nil
	}

	// Get or compute - only runs compute if not in cache
	score, err := cache.GetOrCompute("player:1", computeScore)
	if err != nil {
		fmt.Println("Error:", err)
	}
	fmt.Println("Score:", score)

	// Second call uses cache
	score2, _ := cache.GetOrCompute("player:1", computeScore)
	fmt.Println("Score from cache:", score2)

	// Output:
	// Score: 42
	// Score from cache: 42
}

func ExampleLRUCache_evictionCallback() {
	evicted := make([]string, 0)

	cache := NewLRUCache[string, int](
		WithMaxSize(3),
		WithEvictionCallback(func(key string, value interface{}) {
			evicted = append(evicted, key)
			fmt.Printf("Evicted: %s (value: %d)\n", key, value)
		}),
	)

	// Add 4 items to a cache with size 3
	cache.Set("a", 1)
	cache.Set("b", 2)
	cache.Set("c", 3)
	cache.Set("d", 4) // Triggers eviction of "a"

	// Output:
	// Evicted: a (value: 1)
}

func ExampleLRUCache_stats() {
	cache := NewLRUCache[string, int](
		WithMaxSize(100),
		WithStats(true),
	)

	// Some operations
	cache.Set("a", 1)
	cache.Set("b", 2)
	cache.Get("a") // Hit
	cache.Get("a") // Hit
	cache.Get("c") // Miss

	stats := cache.GetStats()
	fmt.Printf("Hits: %d\n", stats.Hits)
	fmt.Printf("Misses: %d\n", stats.Misses)
	fmt.Printf("Hit Rate: %.1f%%\n", stats.HitRate)
	fmt.Printf("Size: %d\n", stats.Size)

	// Output:
	// Hits: 2
	// Misses: 1
	// Hit Rate: 66.7%
	// Size: 2
}

// ============================================================================
// TTL Cache Examples
// ============================================================================

func ExampleTTLCache_basic() {
	// Create a TTL-only cache (no LRU eviction)
	cache := NewTTLCache[string, string](10 * time.Minute)

	cache.Set("temp:token", "abc123")

	// Set with custom TTL
	cache.SetWithTTL("temp:code", "xyz789", 30*time.Second)

	// Purge expired entries
	purged := cache.PurgeExpired()
	fmt.Printf("Purged %d expired entries\n", purged)
}

// ============================================================================
// Memoization Examples
// ============================================================================

func ExampleMemoize1() {
	// Expensive function to memoize
	fibonacci := Memoize1(func(n int) int {
		if n <= 1 {
			return n
		}
		// Note: in real code, you'd want the memoized version to call itself
		// for proper recursive memoization
		return n * n // Simplified for example
	}, WithMaxSize(100))

	// First call computes
	result1 := fibonacci(5)
	fmt.Println("First call:", result1)

	// Second call uses cache
	result2 := fibonacci(5)
	fmt.Println("Cached call:", result2)

	// Output:
	// First call: 25
	// Cached call: 25
}

func ExampleMemoize1Err() {
	// Function with error handling
	divide := Memoize1Err(func(n int) (int, error) {
		if n == 0 {
			return 0, fmt.Errorf("division by zero")
		}
		return 100 / n, nil
	})

	// Valid call
	result, err := divide(10)
	fmt.Printf("100/10 = %d, err: %v\n", result, err)

	// Cached
	result, err = divide(10)
	fmt.Printf("Cached: %d, err: %v\n", result, err)

	// Error (not cached)
	_, err = divide(0)
	fmt.Printf("Error: %v\n", err)

	// Output:
	// 100/10 = 10, err: <nil>
	// Cached: 10, err: <nil>
	// Error: division by zero
}

func ExampleMemoize2() {
	// Memoize function with two arguments
	add := Memoize2(func(a, b int) int {
		fmt.Printf("Computing %d + %d\n", a, b)
		return a + b
	})

	// First call computes
	fmt.Println("Result:", add(2, 3))

	// Second call uses cache (no print)
	fmt.Println("Result:", add(2, 3))

	// Different args compute again
	fmt.Println("Result:", add(3, 4))

	// Output:
	// Computing 2 + 3
	// Result: 5
	// Result: 5
	// Computing 3 + 4
	// Result: 7
}

// ============================================================================
// Advanced Examples
// ============================================================================

func Example_memoizedFibonacci() {
	// Create a memoized fibonacci calculator
	// Note: This pattern requires the cache to be accessible for recursive calls
	cache := NewLRUCache[int, int](WithMaxSize(100))

	var fib func(n int) int
	fib = func(n int) int {
		// Check cache first
		if val, ok := cache.Get(n); ok {
			return val
		}

		// Base cases
		if n <= 1 {
			cache.Set(n, n)
			return n
		}

		// Recursive case
		result := fib(n-1) + fib(n-2)
		cache.Set(n, result)
		return result
	}

	fmt.Println("fib(10) =", fib(10))
	fmt.Println("fib(20) =", fib(20))

	// Output:
	// fib(10) = 55
	// fib(20) = 6765
}

func Example_apiCache() {
	// Simulating an API response cache
	type User struct {
		ID   int
		Name string
	}

	// Cache API responses for 5 minutes
	userCache := NewLRUCache[int, User](
		WithMaxSize(1000),
		WithTTL(5*time.Minute),
		WithStats(true),
	)

	// Simulated API call
	fetchUser := func(id int) (User, error) {
		// In real code, this would be an HTTP call
		return User{ID: id, Name: fmt.Sprintf("User%d", id)}, nil
	}

	// Get user with caching
	getUser := func(id int) (User, error) {
		return userCache.GetOrCompute(id, func() (User, error) {
			fmt.Printf("Fetching user %d from API...\n", id)
			return fetchUser(id)
		})
	}

	// First call - fetches from API
	user1, _ := getUser(123)
	fmt.Println("User:", user1.Name)

	// Second call - uses cache
	user2, _ := getUser(123)
	fmt.Println("User:", user2.Name)

	// Check stats
	stats := userCache.GetStats()
	fmt.Printf("Hit rate: %.1f%%\n", stats.HitRate)

	// Output:
	// Fetching user 123 from API...
	// User: User123
	// User: User123
	// Hit rate: 50.0%
}

func Example_rateLimiter() {
	// Simple rate limiter using TTL cache
	type RateLimit struct {
		Count     int
		ResetAt   time.Time
	}

	limiter := NewTTLCache[string, RateLimit](1 * time.Minute)

	checkRate := func(ip string, maxRequests int) bool {
		rl, ok := limiter.Get(ip)
		if !ok {
			// First request
			limiter.Set(ip, RateLimit{Count: 1, ResetAt: time.Now().Add(time.Minute)})
			return true
		}

		if rl.Count >= maxRequests {
			return false // Rate limited
		}

		rl.Count++
		limiter.Set(ip, rl)
		return true
	}

	fmt.Println("Request 1:", checkRate("192.168.1.1", 3))
	fmt.Println("Request 2:", checkRate("192.168.1.1", 3))
	fmt.Println("Request 3:", checkRate("192.168.1.1", 3))
	fmt.Println("Request 4:", checkRate("192.168.1.1", 3)) // Should be limited

	// Output:
	// Request 1: true
	// Request 2: true
	// Request 3: true
	// Request 4: false
}

func Example_sessionManager() {
	// Session manager with TTL
	type Session struct {
		UserID    int
		Username  string
		CreatedAt time.Time
	}

	sessions := NewLRUCache[string, Session](
		WithMaxSize(10000),
		WithTTL(30*time.Minute),
		WithEvictionCallback(func(key string, value interface{}) {
			sess := value.(Session)
			fmt.Printf("Session expired for user: %s\n", sess.Username)
		}),
	)

	// Create session
	sessionToken := "abc123xyz"
	sessions.Set(sessionToken, Session{
		UserID:    1,
		Username:  "alice",
		CreatedAt: time.Now(),
	})

	// Validate session
	if sess, ok := sessions.Get(sessionToken); ok {
		fmt.Printf("Active session: %s\n", sess.Username)
	}

	// Logout (delete session)
	sessions.Delete(sessionToken)

	// Output:
	// Active session: alice
	// Session expired for user: alice
}

func Example_deduplication() {
	// Deduplicate expensive operations
	processedCache := NewLRUCache[string, bool](WithTTL(1 * time.Hour))

	processUnique := func(items []string) []string {
		var unique []string
		for _, item := range items {
			if !processedCache.Has(item) {
				unique = append(unique, item)
				processedCache.Set(item, true)
			}
		}
		return unique
	}

	batch1 := []string{"a", "b", "c", "a", "b"}
	unique1 := processUnique(batch1)
	fmt.Println("Batch 1 unique:", unique1)

	batch2 := []string{"a", "b", "d", "e"}
	unique2 := processUnique(batch2)
	fmt.Println("Batch 2 unique:", unique2)

	// Output:
	// Batch 1 unique: [a b c]
	// Batch 2 unique: [d e]
}