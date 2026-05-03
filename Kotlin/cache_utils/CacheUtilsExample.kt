import cache_utils.*

/**
 * Example usage of Cache Utilities
 * 
 * Demonstrates LRU cache, TTL cache, LFU cache, two-level cache, and memoization
 */
fun main() {
    println("=== Cache Utils Examples ===\n")
    
    // ============== LRU Cache Example ==============
    println("1. LRU Cache Example")
    println("-".repeat(40))
    
    val lruCache = LRUCache<String, String>(capacity = 3) { key, value ->
        println("  Evicted: $key -> $value")
    }
    
    lruCache.put("user:1", "Alice")
    lruCache.put("user:2", "Bob")
    lruCache.put("user:3", "Charlie")
    
    println("  Cache size: ${lruCache.size}")
    println("  Get user:1: ${lruCache.get("user:1")}")
    
    // This will cause eviction (user:2 is LRU since we accessed user:1)
    lruCache.put("user:4", "David")
    println("  After adding user:4:")
    println("    user:1: ${lruCache.get("user:1")}") // Exists
    println("    user:2: ${lruCache.get("user:2")}") // Evicted
    println("    user:3: ${lruCache.get("user:3")}") // Exists
    println("    user:4: ${lruCache.get("user:4")}") // Exists
    
    val lruStats = lruCache.getStats()
    println("  Stats: hits=${lruStats.hits}, misses=${lruStats.misses}, hitRate=${"%.2f".format(lruStats.hitRate)}")
    
    println()
    
    // ============== TTL Cache Example ==============
    println("2. TTL Cache Example")
    println("-".repeat(40))
    
    val ttlCache = TTLCache<String, String>(
        defaultTtlMs = 2000L, // 2 seconds
        maxSize = 100
    ) { key, value ->
        println("  Expired: $key -> $value")
    }
    
    ttlCache.put("session:1", "abc123")
    ttlCache.put("session:2", "def456", 500L) // Custom 500ms TTL
    
    println("  Session 1: ${ttlCache.get("session:1")}")
    println("  Session 2: ${ttlCache.get("session:2")}")
    
    println("  Waiting 600ms for session:2 to expire...")
    Thread.sleep(600)
    
    println("  Session 1 (still valid): ${ttlCache.get("session:1")}")
    println("  Session 2 (expired): ${ttlCache.get("session:2")}")
    
    println("  Waiting 1500ms more for session:1 to expire...")
    Thread.sleep(1500)
    
    println("  Session 1 (now expired): ${ttlCache.get("session:1")}")
    
    val ttlStats = ttlCache.getStats()
    println("  Stats: evictions=${ttlStats.evictions}, hitRate=${"%.2f".format(ttlStats.hitRate)}")
    
    println()
    
    // ============== LFU Cache Example ==============
    println("3. LFU Cache Example")
    println("-".repeat(40))
    
    val lfuCache = LFUCache<String, Int>(capacity = 3)
    
    lfuCache.put("a", 1)
    lfuCache.put("b", 2)
    lfuCache.put("c", 3)
    
    // Access 'a' multiple times
    repeat(5) { lfuCache.get("a") }
    
    // Access 'b' fewer times
    repeat(2) { lfuCache.get("b") }
    
    // Don't access 'c'
    
    println("  Access counts: a=6, b=3, c=1")
    
    // Add new item - 'c' has lowest frequency
    lfuCache.put("d", 4)
    
    println("  After adding 'd':")
    println("    a: ${lfuCache.get("a")} (should exist)")
    println("    b: ${lfuCache.get("b")} (should exist)")
    println("    c: ${lfuCache.get("c")} (evicted - lowest frequency)")
    println("    d: ${lfuCache.get("d")} (should exist)")
    
    val lfuStats = lfuCache.getStats()
    println("  Stats: hits=${lfuStats.hits}, misses=${lfuStats.misses}")
    
    println()
    
    // ============== Two-Level Cache Example ==============
    println("4. Two-Level Cache Example")
    println("-".repeat(40))
    
    val twoLevelCache = TwoLevelCache<String, String>(
        lruCapacity = 2,
        ttlCapacity = 5,
        defaultTtlMs = 5000L
    )
    
    twoLevelCache.put("item:1", "Value 1")
    twoLevelCache.put("item:2", "Value 2")
    twoLevelCache.put("item:3", "Value 3") // item:1 evicted from L1
    
    println("  L1 (fast, small): items 2, 3")
    println("  L2 (larger, with TTL): items 1, 2, 3")
    
    println("  Get item:1: ${twoLevelCache.get("item:1")}") // Fetched from L2, promoted to L1
    println("  Get item:2: ${twoLevelCache.get("item:2")}") // From L1
    
    val twoLevelStats = twoLevelCache.getStats()
    println("  L1 Stats: ${twoLevelStats.l1Stats}")
    println("  L2 Stats: ${twoLevelStats.l2Stats}")
    
    println()
    
    // ============== MemoCache Example ==============
    println("5. MemoCache Example")
    println("-".repeat(40))
    
    var fibonacciComputeCount = 0
    
    // Memoized Fibonacci
    val fibCache = MemoCache<Int, Long> { n ->
        fibonacciComputeCount++
        println("    Computing fib($n)...")
        when {
            n <= 0 -> 0L
            n == 1 -> 1L
            else -> {
                // Note: This naive implementation will still cause multiple computations
                // because we can't reference the cache inside the lambda
                var a = 0L
                var b = 1L
                repeat(n - 1) {
                    val temp = a + b
                    a = b
                    b = temp
                }
                b
            }
        }
    }
    
    println("  Computing fib(20):")
    val fib20 = fibCache.get(20)
    println("  Result: $fib20")
    println("  Computations: $fibonacciComputeCount")
    
    // Second call should use cached value
    println("  Getting fib(20) again:")
    val fib20Again = fibCache.get(20)
    println("  Result: $fib20Again")
    println("  Computations: $fibonacciComputeCount (unchanged - used cache)")
    
    println()
    
    // ============== Practical Use Case: API Response Cache ==============
    println("6. Practical Example: API Response Cache")
    println("-".repeat(40))
    
    // Simulate an API response cache with TTL
    data class ApiResponse(val data: String, val timestamp: Long)
    
    val apiCache = TTLCache<String, ApiResponse>(
        defaultTtlMs = 30000L, // 30 seconds
        maxSize = 100
    )
    
    // Simulate API call
    fun fetchUser(id: String): ApiResponse {
        // Check cache first
        apiCache.get("user:$id")?.let {
            println("  [CACHE HIT] User $id from cache")
            return it
        }
        
        // Simulate API delay
        println("  [API CALL] Fetching user $id from server...")
        Thread.sleep(100)
        
        val response = ApiResponse(
            data = "User(id=$id, name=User$id)",
            timestamp = System.currentTimeMillis()
        )
        
        apiCache.put("user:$id", response)
        return response
    }
    
    println("  First request:")
    fetchUser("123")
    
    println("  Second request (should hit cache):")
    fetchUser("123")
    
    println()
    
    // ============== Stats Summary ==============
    println("=== Cache Statistics Summary ===")
    println()
    
    println("LRU Cache:")
    println("  - Capacity-based eviction")
    println("  - Best for: Recent access patterns")
    
    println("TTL Cache:")
    println("  - Time-based expiration")
    println("  - Best for: Data that becomes stale")
    
    println("LFU Cache:")
    println("  - Frequency-based eviction")
    println("  - Best for: Hot data patterns")
    
    println("Two-Level Cache:")
    println("  - Combines LRU speed with TTL persistence")
    println("  - Best for: Multi-tier caching")
    
    println("MemoCache:")
    println("  - Function result caching")
    println("  - Best for: Expensive computations")
    
    println("\nAll examples completed successfully!")
}