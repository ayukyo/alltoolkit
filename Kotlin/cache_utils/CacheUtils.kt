/**
 * Cache Utilities for Kotlin
 * 
 * Provides efficient caching implementations with zero external dependencies.
 * Includes LRU cache, TTL cache, and composite cache with memory management.
 * 
 * @author AllToolkit
 * @date 2026-05-03
 */

package cache_utils

import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.ConcurrentLinkedDeque
import java.util.concurrent.atomic.AtomicLong
import java.util.concurrent.locks.ReentrantLock
import kotlin.concurrent.withLock

/**
 * LRU (Least Recently Used) Cache implementation
 * Automatically evicts least recently used entries when capacity is reached
 */
class LRUCache<K, V>(
    private val capacity: Int,
    private val onEvict: ((K, V) -> Unit)? = null
) {
    init {
        require(capacity > 0) { "Capacity must be positive" }
    }
    
    private val cache = ConcurrentHashMap<K, V>()
    private val accessOrder = ConcurrentLinkedDeque<K>()
    private val lock = ReentrantLock()
    
    @Volatile
    private var hitCount = AtomicLong(0)
    
    @Volatile
    private var missCount = AtomicLong(0)
    
    /**
     * Get a value from the cache
     * @param key The key to look up
     * @return The value if found, null otherwise
     */
    fun get(key: K): V? {
        return lock.withLock {
            val value = cache[key]
            if (value != null) {
                hitCount.incrementAndGet()
                // Move to front (most recently used)
                accessOrder.remove(key)
                accessOrder.addFirst(key)
                value
            } else {
                missCount.incrementAndGet()
                null
            }
        }
    }
    
    /**
     * Put a value into the cache
     * @param key The key to store
     * @param value The value to store
     * @return The evicted value if any, null otherwise
     */
    fun put(key: K, value: V): V? {
        return lock.withLock {
            // If key exists, remove it from access order first
            if (cache.containsKey(key)) {
                accessOrder.remove(key)
            }
            
            // If at capacity, evict LRU entry
            var evictedValue: V? = null
            while (cache.size >= capacity && accessOrder.isNotEmpty()) {
                val lruKey = accessOrder.removeLast()
                evictedValue = cache.remove(lruKey)
                evictedValue?.let { onEvict?.invoke(lruKey, it) }
            }
            
            cache[key] = value
            accessOrder.addFirst(key)
            evictedValue
        }
    }
    
    /**
     * Remove a key from the cache
     * @param key The key to remove
     * @return The removed value if any, null otherwise
     */
    fun remove(key: K): V? {
        return lock.withLock {
            val value = cache.remove(key)
            if (value != null) {
                accessOrder.remove(key)
            }
            value
        }
    }
    
    /**
     * Check if a key exists in the cache
     */
    fun contains(key: K): Boolean = cache.containsKey(key)
    
    /**
     * Clear all entries from the cache
     */
    fun clear() {
        lock.withLock {
            cache.clear()
            accessOrder.clear()
        }
    }
    
    /**
     * Get the current size of the cache
     */
    val size: Int get() = cache.size
    
    /**
     * Get cache statistics
     */
    fun getStats(): CacheStats {
        val hits = hitCount.get()
        val misses = missCount.get()
        return CacheStats(
            size = size,
            capacity = capacity,
            hits = hits,
            misses = misses,
            hitRate = if (hits + misses > 0) hits.toDouble() / (hits + misses) else 0.0
        )
    }
}

/**
 * TTL (Time-To-Live) Cache implementation
 * Entries automatically expire after a specified duration
 */
class TTLCache<K, V>(
    private val defaultTtlMs: Long = 60_000L, // 1 minute default
    private val maxSize: Int = 1000,
    private val onExpire: ((K, V) -> Unit)? = null
) {
    private data class Entry<V>(
        val value: V,
        val expiresAt: Long
    ) {
        fun isExpired(): Boolean = System.currentTimeMillis() > expiresAt
    }
    
    private val cache = ConcurrentHashMap<K, Entry<V>>()
    private val lock = ReentrantLock()
    
    @Volatile
    private var hitCount = AtomicLong(0)
    
    @Volatile
    private var missCount = AtomicLong(0)
    
    @Volatile
    private var evictionCount = AtomicLong(0)
    
    /**
     * Get a value from the cache
     * @param key The key to look up
     * @return The value if found and not expired, null otherwise
     */
    fun get(key: K): V? {
        return lock.withLock {
            val entry = cache[key]
            if (entry != null) {
                if (entry.isExpired()) {
                    cache.remove(key)
                    evictionCount.incrementAndGet()
                    onExpire?.invoke(key, entry.value)
                    missCount.incrementAndGet()
                    null
                } else {
                    hitCount.incrementAndGet()
                    entry.value
                }
            } else {
                missCount.incrementAndGet()
                null
            }
        }
    }
    
    /**
     * Put a value into the cache with default TTL
     * @param key The key to store
     * @param value The value to store
     */
    fun put(key: K, value: V) {
        put(key, value, defaultTtlMs)
    }
    
    /**
     * Put a value into the cache with custom TTL
     * @param key The key to store
     * @param value The value to store
     * @param ttlMs Time to live in milliseconds
     */
    fun put(key: K, value: V, ttlMs: Long) {
        lock.withLock {
            // Cleanup if approaching max size
            if (cache.size >= maxSize) {
                cleanupExpired()
                if (cache.size >= maxSize) {
                    // Force eviction of oldest entries
                    val toRemove = cache.size - maxSize + 1
                    cache.entries
                        .sortedBy { it.value.expiresAt }
                        .take(toRemove)
                        .forEach { (k, v) ->
                            cache.remove(k)
                            evictionCount.incrementAndGet()
                            onExpire?.invoke(k, v.value)
                        }
                }
            }
            
            cache[key] = Entry(value, System.currentTimeMillis() + ttlMs)
        }
    }
    
    /**
     * Remove a key from the cache
     */
    fun remove(key: K): V? {
        return lock.withLock {
            cache.remove(key)?.value
        }
    }
    
    /**
     * Check if a key exists and is not expired
     */
    fun contains(key: K): Boolean {
        return get(key) != null
    }
    
    /**
     * Clean up all expired entries
     * @return Number of entries removed
     */
    fun cleanupExpired(): Int {
        return lock.withLock {
            var removed = 0
            val iterator = cache.entries.iterator()
            while (iterator.hasNext()) {
                val entry = iterator.next()
                if (entry.value.isExpired()) {
                    iterator.remove()
                    removed++
                    onExpire?.invoke(entry.key, entry.value.value)
                }
            }
            evictionCount.addAndGet(removed.toLong())
            removed
        }
    }
    
    /**
     * Clear all entries from the cache
     */
    fun clear() {
        lock.withLock {
            cache.clear()
        }
    }
    
    /**
     * Get the current size of the cache (including potentially expired entries)
     */
    val size: Int get() = cache.size
    
    /**
     * Get cache statistics
     */
    fun getStats(): TTLCacheStats {
        val hits = hitCount.get()
        val misses = missCount.get()
        val evictions = evictionCount.get()
        return TTLCacheStats(
            size = size,
            maxSize = maxSize,
            hits = hits,
            misses = misses,
            hitRate = if (hits + misses > 0) hits.toDouble() / (hits + misses) else 0.0,
            evictions = evictions,
            defaultTtlMs = defaultTtlMs
        )
    }
}

/**
 * LFU (Least Frequently Used) Cache implementation
 * Evicts entries that are accessed least frequently
 */
class LFUCache<K, V>(
    private val capacity: Int,
    private val onEvict: ((K, V) -> Unit)? = null
) {
    init {
        require(capacity > 0) { "Capacity must be positive" }
    }
    
    private data class Entry<V>(
        val value: V,
        var frequency: Long = 1
    )
    
    private val cache = ConcurrentHashMap<K, Entry<V>>()
    private val lock = ReentrantLock()
    
    @Volatile
    private var hitCount = AtomicLong(0)
    
    @Volatile
    private var missCount = AtomicLong(0)
    
    /**
     * Get a value from the cache
     * Increments access frequency on hit
     */
    fun get(key: K): V? {
        return lock.withLock {
            val entry = cache[key]
            if (entry != null) {
                hitCount.incrementAndGet()
                entry.frequency++
                entry.value
            } else {
                missCount.incrementAndGet()
                null
            }
        }
    }
    
    /**
     * Put a value into the cache
     * Evicts least frequently used entry if at capacity
     */
    fun put(key: K, value: V): V? {
        return lock.withLock {
            // If key exists, update value and reset frequency
            if (cache.containsKey(key)) {
                cache[key] = Entry(value)
                return@withLock null
            }
            
            // If at capacity, evict LFU entry
            var evictedValue: V? = null
            if (cache.size >= capacity) {
                val lfuKey = cache.entries
                    .minByOrNull { it.value.frequency }
                    ?.key
                if (lfuKey != null) {
                    evictedValue = cache.remove(lfuKey)?.value
                    evictedValue?.let { onEvict?.invoke(lfuKey, it) }
                }
            }
            
            cache[key] = Entry(value)
            evictedValue
        }
    }
    
    /**
     * Remove a key from the cache
     */
    fun remove(key: K): V? {
        return lock.withLock {
            cache.remove(key)?.value
        }
    }
    
    /**
     * Check if a key exists in the cache
     */
    fun contains(key: K): Boolean = cache.containsKey(key)
    
    /**
     * Clear all entries
     */
    fun clear() {
        lock.withLock {
            cache.clear()
        }
    }
    
    /**
     * Get current size
     */
    val size: Int get() = cache.size
    
    /**
     * Get cache statistics
     */
    fun getStats(): CacheStats {
        val hits = hitCount.get()
        val misses = missCount.get()
        return CacheStats(
            size = size,
            capacity = capacity,
            hits = hits,
            misses = misses,
            hitRate = if (hits + misses > 0) hits.toDouble() / (hits + misses) else 0.0
        )
    }
}

/**
 * Two-Level Cache combining LRU and TTL
 * L1: Fast access, limited size (LRU)
 * L2: Longer storage with TTL
 */
class TwoLevelCache<K, V>(
    lruCapacity: Int = 100,
    ttlCapacity: Int = 1000,
    defaultTtlMs: Long = 300_000L // 5 minutes
) {
    private val l1Cache = LRUCache<K, V>(lruCapacity)
    private val l2Cache = TTLCache<K, V>(defaultTtlMs, ttlCapacity)
    
    /**
     * Get from L1 first, then L2
     */
    fun get(key: K): V? {
        // Try L1 first
        l1Cache.get(key)?.let { return it }
        
        // Try L2
        return l2Cache.get(key)?.also { 
            // Promote to L1 on hit
            l1Cache.put(key, it)
        }
    }
    
    /**
     * Put in both levels
     */
    fun put(key: K, value: V) {
        l1Cache.put(key, value)
        l2Cache.put(key, value)
    }
    
    /**
     * Put with custom TTL
     */
    fun put(key: K, value: V, ttlMs: Long) {
        l1Cache.put(key, value)
        l2Cache.put(key, value, ttlMs)
    }
    
    /**
     * Remove from both levels
     */
    fun remove(key: K): Boolean {
        val fromL1 = l1Cache.remove(key) != null
        val fromL2 = l2Cache.remove(key) != null
        return fromL1 || fromL2
    }
    
    /**
     * Clear both levels
     */
    fun clear() {
        l1Cache.clear()
        l2Cache.clear()
    }
    
    /**
     * Get combined stats
     */
    fun getStats(): TwoLevelCacheStats {
        return TwoLevelCacheStats(
            l1Stats = l1Cache.getStats(),
            l2Stats = l2Cache.getStats()
        )
    }
}

/**
 * Cache statistics data class
 */
data class CacheStats(
    val size: Int,
    val capacity: Int,
    val hits: Long,
    val misses: Long,
    val hitRate: Double
)

/**
 * TTL Cache statistics data class
 */
data class TTLCacheStats(
    val size: Int,
    val maxSize: Int,
    val hits: Long,
    val misses: Long,
    val hitRate: Double,
    val evictions: Long,
    val defaultTtlMs: Long
)

/**
 * Two-level cache statistics
 */
data class TwoLevelCacheStats(
    val l1Stats: CacheStats,
    val l2Stats: TTLCacheStats
)

/**
 * Simple memoization cache for function results
 */
class MemoCache<K, V>(
    private val compute: (K) -> V
) {
    private val cache = ConcurrentHashMap<K, V>()
    
    fun get(key: K): V = cache.computeIfAbsent(key, compute)
    
    fun clear() = cache.clear()
    
    val size: Int get() = cache.size
    
    fun contains(key: K): Boolean = cache.containsKey(key)
}