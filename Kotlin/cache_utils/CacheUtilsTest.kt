import cache_utils.*
import org.junit.Assert.*
import org.junit.Test
import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicInteger

/**
 * Test suite for Cache Utilities
 */
class CacheUtilsTest {
    
    // ============== LRU Cache Tests ==============
    
    @Test
    fun testLRUCacheBasicOperations() {
        val cache = LRUCache<String, Int>(3)
        
        assertEquals(0, cache.size)
        assertFalse(cache.contains("a"))
        
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        
        assertEquals(3, cache.size)
        assertEquals(1, cache.get("a"))
        assertEquals(2, cache.get("b"))
        assertEquals(3, cache.get("c"))
    }
    
    @Test
    fun testLRUCacheEviction() {
        val cache = LRUCache<String, Int>(2)
        
        cache.put("a", 1)
        cache.put("b", 2)
        
        // Access "a" to make it recently used
        cache.get("a")
        
        // Add new item, should evict "b" (least recently used)
        cache.put("c", 3)
        
        assertEquals(2, cache.size)
        assertEquals(1, cache.get("a")) // "a" still exists
        assertNull(cache.get("b")) // "b" was evicted
        assertEquals(3, cache.get("c")) // "c" exists
    }
    
    @Test
    fun testLRUCacheUpdate() {
        val cache = LRUCache<String, Int>(2)
        
        cache.put("a", 1)
        cache.put("a", 2)
        
        assertEquals(1, cache.size)
        assertEquals(2, cache.get("a"))
    }
    
    @Test
    fun testLRUCacheRemove() {
        val cache = LRUCache<String, Int>(3)
        
        cache.put("a", 1)
        cache.put("b", 2)
        
        assertEquals(1, cache.remove("a"))
        assertNull(cache.get("a"))
        assertEquals(1, cache.size)
    }
    
    @Test
    fun testLRUCacheClear() {
        val cache = LRUCache<String, Int>(3)
        
        cache.put("a", 1)
        cache.put("b", 2)
        cache.clear()
        
        assertEquals(0, cache.size)
    }
    
    @Test
    fun testLRUCacheStats() {
        val cache = LRUCache<String, Int>(3)
        
        cache.put("a", 1)
        cache.get("a") // hit
        cache.get("a") // hit
        cache.get("b") // miss
        
        val stats = cache.getStats()
        assertEquals(1, stats.size)
        assertEquals(3, stats.capacity)
        assertEquals(2L, stats.hits)
        assertEquals(1L, stats.misses)
        assertEquals(2.0 / 3.0, stats.hitRate, 0.001)
    }
    
    @Test
    fun testLRUCacheEvictionCallback() {
        val evicted = mutableListOf<Pair<String, Int>>()
        val cache = LRUCache<String, Int>(2) { key, value ->
            evicted.add(key to value)
        }
        
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3) // Should evict "a"
        
        assertEquals(1, evicted.size)
        assertEquals("a" to 1, evicted[0])
    }
    
    @Test(expected = IllegalArgumentException::class)
    fun testLRUCacheInvalidCapacity() {
        LRUCache<String, Int>(0)
    }
    
    @Test
    fun testLRUCacheThreadSafety() {
        val cache = LRUCache<Int, Int>(100)
        val executor = Executors.newFixedThreadPool(10)
        val latch = CountDownLatch(100)
        
        repeat(100) { i ->
            executor.submit {
                cache.put(i, i)
                cache.get(i)
                latch.countDown()
            }
        }
        
        latch.await(10, TimeUnit.SECONDS)
        executor.shutdown()
        
        // All operations should complete without exceptions
        assertTrue(cache.size <= 100)
    }
    
    // ============== TTL Cache Tests ==============
    
    @Test
    fun testTTLCacheBasicOperations() {
        val cache = TTLCache<String, Int>(60_000L, 10)
        
        cache.put("a", 1)
        
        assertEquals(1, cache.get("a"))
        assertTrue(cache.contains("a"))
    }
    
    @Test
    fun testTTLCacheExpiration() {
        val cache = TTLCache<String, Int>(100L, 10) // 100ms TTL
        
        cache.put("a", 1)
        
        // Should exist immediately
        assertEquals(1, cache.get("a"))
        
        // Wait for expiration
        Thread.sleep(150)
        
        // Should be expired
        assertNull(cache.get("a"))
    }
    
    @Test
    fun testTTLCacheCustomTTL() {
        val cache = TTLCache<String, Int>(60_000L, 10)
        
        cache.put("a", 1, 100L) // 100ms TTL
        
        assertEquals(1, cache.get("a"))
        
        Thread.sleep(150)
        
        assertNull(cache.get("a"))
    }
    
    @Test
    fun testTTLCacheCleanup() {
        val cache = TTLCache<String, Int>(100L, 10)
        
        cache.put("a", 1)
        cache.put("b", 2)
        
        Thread.sleep(150)
        
        // Manual cleanup
        val removed = cache.cleanupExpired()
        
        assertEquals(2, removed)
        assertEquals(0, cache.size)
    }
    
    @Test
    fun testTTLCacheExpirationCallback() {
        val expired = mutableListOf<Pair<String, Int>>()
        val cache = TTLCache<String, Int>(100L, 10) { key, value ->
            expired.add(key to value)
        }
        
        cache.put("a", 1)
        
        Thread.sleep(150)
        
        // Access expired entry
        assertNull(cache.get("a"))
        
        assertEquals(1, expired.size)
        assertEquals("a" to 1, expired[0])
    }
    
    @Test
    fun testTTLCacheStats() {
        val cache = TTLCache<String, Int>(60_000L, 10)
        
        cache.put("a", 1)
        cache.get("a") // hit
        cache.get("b") // miss
        
        val stats = cache.getStats()
        assertEquals(1, stats.size)
        assertEquals(10, stats.maxSize)
        assertEquals(1L, stats.hits)
        assertEquals(1L, stats.misses)
    }
    
    // ============== LFU Cache Tests ==============
    
    @Test
    fun testLFUCacheBasicOperations() {
        val cache = LFUCache<String, Int>(3)
        
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        
        assertEquals(3, cache.size)
        assertEquals(1, cache.get("a"))
        assertEquals(2, cache.get("b"))
        assertEquals(3, cache.get("c"))
    }
    
    @Test
    fun testLFUCacheEviction() {
        val cache = LFUCache<String, Int>(2)
        
        cache.put("a", 1)
        cache.put("b", 2)
        
        // Access "a" multiple times to increase its frequency
        cache.get("a")
        cache.get("a")
        cache.get("a")
        
        // Access "b" once
        cache.get("b")
        
        // Add new item, should evict "b" (lower frequency)
        cache.put("c", 3)
        
        assertEquals(2, cache.size)
        assertEquals(1, cache.get("a")) // "a" still exists
        assertNull(cache.get("b")) // "b" was evicted
        assertEquals(3, cache.get("c"))
    }
    
    @Test
    fun testLFUCacheUpdateResetsFrequency() {
        val cache = LFUCache<String, Int>(2)
        
        cache.put("a", 1)
        cache.get("a") // frequency = 2
        cache.get("a") // frequency = 3
        
        cache.put("a", 100) // Reset to frequency = 1
        
        cache.put("b", 2)
        cache.get("b")
        cache.get("b") // frequency = 3
        
        // Add new item, should evict "a" (lower frequency after reset)
        cache.put("c", 3)
        
        assertNull(cache.get("a")) // "a" was evicted
    }
    
    @Test
    fun testLFUCacheStats() {
        val cache = LFUCache<String, Int>(3)
        
        cache.put("a", 1)
        cache.get("a") // hit
        cache.get("b") // miss
        
        val stats = cache.getStats()
        assertEquals(1L, stats.hits)
        assertEquals(1L, stats.misses)
    }
    
    // ============== Two-Level Cache Tests ==============
    
    @Test
    fun testTwoLevelCacheBasicOperations() {
        val cache = TwoLevelCache<String, Int>()
        
        cache.put("a", 1)
        
        assertEquals(1, cache.get("a"))
    }
    
    @Test
    fun testTwoLevelCachePromotion() {
        val cache = TwoLevelCache<String, Int>(
            lruCapacity = 2,
            ttlCapacity = 10,
            defaultTtlMs = 60_000L
        )
        
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3) // "a" evicted from L1
        
        // "a" should still be in L2
        val fromL2 = cache.get("a")
        assertNotNull(fromL2) // Found in L2 and promoted to L1
        assertEquals(1, fromL2)
    }
    
    @Test
    fun testTwoLevelCacheCustomTTL() {
        val cache = TwoLevelCache<String, Int>(
            lruCapacity = 10,
            ttlCapacity = 100,
            defaultTtlMs = 200L // 200ms TTL
        )
        
        cache.put("a", 1, 200L) // 200ms TTL
        
        assertEquals(1, cache.get("a"))
        
        // Wait for TTL to expire (L2)
        Thread.sleep(300)
        
        // L2 expired, but L1 still has data
        // When L1 evicts and we try to get from L2, it will be null
        // Fill L1 to force eviction
        repeat(10) { i ->
            cache.put("b$i", i)
        }
        
        // Now "a" should be evicted from L1 and expired from L2
        assertNull(cache.get("a"))
    }
    
    @Test
    fun testTwoLevelCacheRemove() {
        val cache = TwoLevelCache<String, Int>()
        
        cache.put("a", 1)
        assertTrue(cache.remove("a"))
        assertNull(cache.get("a"))
    }
    
    @Test
    fun testTwoLevelCacheClear() {
        val cache = TwoLevelCache<String, Int>()
        
        cache.put("a", 1)
        cache.put("b", 2)
        cache.clear()
        
        assertNull(cache.get("a"))
        assertNull(cache.get("b"))
    }
    
    // ============== MemoCache Tests ==============
    
    @Test
    fun testMemoCacheBasic() {
        var computeCount = 0
        val cache = MemoCache<String, Int> { key ->
            computeCount++
            key.length
        }
        
        assertEquals(4, cache.get("test"))
        assertEquals(1, computeCount)
        
        // Should not recompute
        assertEquals(4, cache.get("test"))
        assertEquals(1, computeCount)
        
        assertEquals(5, cache.get("hello"))
        assertEquals(2, computeCount)
    }
    
    @Test
    fun testMemoCacheContains() {
        val cache = MemoCache<String, Int> { it.length }
        
        assertFalse(cache.contains("test"))
        cache.get("test")
        assertTrue(cache.contains("test"))
    }
    
    @Test
    fun testMemoCacheClear() {
        val cache = MemoCache<String, Int> { it.length }
        
        cache.get("test")
        assertEquals(1, cache.size)
        
        cache.clear()
        assertEquals(0, cache.size)
    }
    
    @Test
    fun testMemoCacheThreadSafety() {
        val computeCount = AtomicInteger(0)
        val cache = MemoCache<Int, Int> { key ->
            computeCount.incrementAndGet()
            key * 2
        }
        
        val executor = Executors.newFixedThreadPool(10)
        val latch = CountDownLatch(100)
        
        repeat(100) { i ->
            executor.submit {
                cache.get(i % 10) // Only 10 unique keys
                latch.countDown()
            }
        }
        
        latch.await(10, TimeUnit.SECONDS)
        executor.shutdown()
        
        // Each key should only be computed once
        assertEquals(10, computeCount.get())
        assertEquals(10, cache.size)
    }
    
    // ============== Performance Tests ==============
    
    @Test
    fun testLRUCachePerformance() {
        val cache = LRUCache<Int, Int>(10000)
        val startTime = System.currentTimeMillis()
        
        repeat(10000) { i ->
            cache.put(i, i)
        }
        
        repeat(10000) { i ->
            cache.get(i)
        }
        
        val elapsed = System.currentTimeMillis() - startTime
        println("LRU Cache 10000 puts + 10000 gets: ${elapsed}ms")
        
        // Should complete in reasonable time
        assertTrue(elapsed < 5000)
    }
    
    @Test
    fun testTTLCachePerformance() {
        val cache = TTLCache<Int, Int>(60_000L, 10000)
        val startTime = System.currentTimeMillis()
        
        repeat(10000) { i ->
            cache.put(i, i)
        }
        
        repeat(10000) { i ->
            cache.get(i)
        }
        
        val elapsed = System.currentTimeMillis() - startTime
        println("TTL Cache 10000 puts + 10000 gets: ${elapsed}ms")
        
        // Should complete in reasonable time
        assertTrue(elapsed < 5000)
    }
}