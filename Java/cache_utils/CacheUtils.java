// CacheUtils - In-Memory Cache with TTL Support
// Zero external dependencies - pure Java implementation

import java.time.Instant;
import java.time.Duration;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.function.Supplier;

/**
 * A thread-safe in-memory cache with TTL (Time-To-Live) support.
 * Zero external dependencies - uses only Java standard library.
 * 
 * Features:
 * - Thread-safe operations using ConcurrentHashMap
 * - Automatic expiration with TTL support
 * - Optional background cleanup of expired entries
 * - Get-or-compute pattern for cache miss handling
 * - Cache statistics (hits, misses, size)
 * - Support for different eviction policies
 * 
 * @author AllToolkit
 * @version 1.0.0
 */
public class CacheUtils {

    // Main cache storage
    private final ConcurrentHashMap<String, CacheEntry<?>> cache;
    
    // Scheduled executor for background cleanup
    private final ScheduledExecutorService cleanupExecutor;
    
    // Default TTL in milliseconds
    private final long defaultTtlMillis;
    
    // Maximum cache size (0 = unlimited)
    private final int maxSize;
    
    // Statistics
    private long hitCount = 0;
    private long missCount = 0;

    /**
     * Internal cache entry that stores value and expiration time.
     */
    private static class CacheEntry<T> {
        private final T value;
        private final long expiresAtMillis;
        private final long createdAtMillis;

        CacheEntry(T value, long ttlMillis) {
            this.value = value;
            this.createdAtMillis = System.currentTimeMillis();
            this.expiresAtMillis = ttlMillis > 0 
                ? this.createdAtMillis + ttlMillis 
                : Long.MAX_VALUE;
        }

        boolean isExpired() {
            return System.currentTimeMillis() > expiresAtMillis;
        }

        long getRemainingTtlMillis() {
            return Math.max(0, expiresAtMillis - System.currentTimeMillis());
        }

        long getAgeMillis() {
            return System.currentTimeMillis() - createdAtMillis;
        }
    }

    /**
     * Builder for creating CacheUtils instances with custom configuration.
     */
    public static class Builder {
        private long defaultTtlMillis = 0; // No expiration by default
        private int maxSize = 0; // Unlimited
        private long cleanupIntervalMillis = 0; // No background cleanup
        private boolean enableCleanup = false;

        /**
         * Set the default TTL for cache entries.
         * @param duration TTL duration
         * @return this builder
         */
        public Builder defaultTtl(Duration duration) {
            this.defaultTtlMillis = duration.toMillis();
            return this;
        }

        /**
         * Set the default TTL in milliseconds.
         * @param millis TTL in milliseconds
         * @return this builder
         */
        public Builder defaultTtlMillis(long millis) {
            this.defaultTtlMillis = millis;
            return this;
        }

        /**
         * Set maximum cache size.
         * @param maxSize maximum number of entries (0 = unlimited)
         * @return this builder
         */
        public Builder maxSize(int maxSize) {
            this.maxSize = maxSize;
            return this;
        }

        /**
         * Enable automatic background cleanup of expired entries.
         * @param intervalMillis cleanup interval in milliseconds
         * @return this builder
         */
        public Builder enableCleanup(long intervalMillis) {
            this.enableCleanup = true;
            this.cleanupIntervalMillis = intervalMillis;
            return this;
        }

        /**
         * Build the CacheUtils instance.
         * @return new CacheUtils instance
         */
        public CacheUtils build() {
            return new CacheUtils(defaultTtlMillis, maxSize, enableCleanup, cleanupIntervalMillis);
        }
    }

    /**
     * Create a new builder for CacheUtils.
     * @return new Builder instance
     */
    public static Builder builder() {
        return new Builder();
    }

    /**
     * Create a new CacheUtils with default settings (no TTL, unlimited size).
     */
    public CacheUtils() {
        this(0, 0, false, 0);
    }

    /**
     * Create a new CacheUtils with specified default TTL.
     * @param defaultTtlMillis default TTL in milliseconds
     */
    public CacheUtils(long defaultTtlMillis) {
        this(defaultTtlMillis, 0, false, 0);
    }

    private CacheUtils(long defaultTtlMillis, int maxSize, boolean enableCleanup, long cleanupIntervalMillis) {
        this.cache = new ConcurrentHashMap<>();
        this.defaultTtlMillis = defaultTtlMillis;
        this.maxSize = maxSize;
        
        if (enableCleanup && cleanupIntervalMillis > 0) {
            this.cleanupExecutor = Executors.newSingleThreadScheduledExecutor(r -> {
                Thread t = new Thread(r, "CacheUtils-Cleanup");
                t.setDaemon(true);
                return t;
            });
            this.cleanupExecutor.scheduleAtFixedRate(
                this::cleanupExpired,
                cleanupIntervalMillis,
                cleanupIntervalMillis,
                TimeUnit.MILLISECONDS
            );
        } else {
            this.cleanupExecutor = null;
        }
    }

    /**
     * Store a value in the cache with default TTL.
     * @param key cache key
     * @param value value to store
     * @param <T> value type
     */
    public <T> void put(String key, T value) {
        put(key, value, defaultTtlMillis);
    }

    /**
     * Store a value in the cache with specified TTL.
     * @param key cache key
     * @param value value to store
     * @param ttlMillis TTL in milliseconds
     * @param <T> value type
     */
    public <T> void put(String key, T value, long ttlMillis) {
        enforceMaxSize();
        cache.put(key, new CacheEntry<>(value, ttlMillis));
    }

    /**
     * Store a value in the cache with Duration TTL.
     * @param key cache key
     * @param value value to store
     * @param ttl TTL duration
     * @param <T> value type
     */
    public <T> void put(String key, T value, Duration ttl) {
        put(key, value, ttl.toMillis());
    }

    /**
     * Get a value from the cache.
     * @param key cache key
     * @param <T> value type
     * @return Optional containing the value if present and not expired
     */
    @SuppressWarnings("unchecked")
    public <T> Optional<T> get(String key) {
        CacheEntry<?> entry = cache.get(key);
        
        if (entry == null) {
            missCount++;
            return Optional.empty();
        }
        
        if (entry.isExpired()) {
            cache.remove(key);
            missCount++;
            return Optional.empty();
        }
        
        hitCount++;
        return Optional.ofNullable((T) entry.value);
    }

    /**
     * Get a value from the cache, or compute and store it if absent.
     * @param key cache key
     * @param supplier function to compute value if absent
     * @param <T> value type
     * @return cached or computed value
     */
    public <T> T getOrCompute(String key, Supplier<T> supplier) {
        return getOrCompute(key, supplier, defaultTtlMillis);
    }

    /**
     * Get a value from the cache, or compute and store it with specified TTL.
     * @param key cache key
     * @param supplier function to compute value if absent
     * @param ttlMillis TTL for newly computed value
     * @param <T> value type
     * @return cached or computed value
     */
    @SuppressWarnings("unchecked")
    public <T> T getOrCompute(String key, Supplier<T> supplier, long ttlMillis) {
        CacheEntry<?> entry = cache.get(key);
        
        if (entry != null && !entry.isExpired()) {
            hitCount++;
            return (T) entry.value;
        }
        
        missCount++;
        T value = supplier.get();
        put(key, value, ttlMillis);
        return value;
    }

    /**
     * Check if a key exists in the cache (and is not expired).
     * @param key cache key
     * @return true if key exists and is not expired
     */
    public boolean contains(String key) {
        CacheEntry<?> entry = cache.get(key);
        if (entry == null) return false;
        if (entry.isExpired()) {
            cache.remove(key);
            return false;
        }
        return true;
    }

    /**
     * Remove a key from the cache.
     * @param key cache key
     * @return true if the key was present
     */
    public boolean remove(String key) {
        return cache.remove(key) != null;
    }

    /**
     * Clear all entries from the cache.
     */
    public void clear() {
        cache.clear();
        hitCount = 0;
        missCount = 0;
    }

    /**
     * Get the current cache size.
     * @return number of entries in cache
     */
    public int size() {
        return cache.size();
    }

    /**
     * Get the remaining TTL for a key.
     * @param key cache key
     * @return remaining TTL in milliseconds, or empty if key not found
     */
    public Optional<Long> getRemainingTtl(String key) {
        CacheEntry<?> entry = cache.get(key);
        if (entry == null || entry.isExpired()) {
            return Optional.empty();
        }
        return Optional.of(entry.getRemainingTtlMillis());
    }

    /**
     * Get the age of a cached entry.
     * @param key cache key
     * @return age in milliseconds, or empty if key not found
     */
    public Optional<Long> getAge(String key) {
        CacheEntry<?> entry = cache.get(key);
        if (entry == null || entry.isExpired()) {
            return Optional.empty();
        }
        return Optional.of(entry.getAgeMillis());
    }

    /**
     * Manually trigger cleanup of expired entries.
     */
    public void cleanupExpired() {
        cache.entrySet().removeIf(entry -> entry.getValue().isExpired());
    }

    /**
     * Get cache hit count.
     * @return number of cache hits
     */
    public long getHitCount() {
        return hitCount;
    }

    /**
     * Get cache miss count.
     * @return number of cache misses
     */
    public long getMissCount() {
        return missCount;
    }

    /**
     * Get cache hit rate.
     * @return hit rate (0.0 to 1.0)
     */
    public double getHitRate() {
        long total = hitCount + missCount;
        return total == 0 ? 0.0 : (double) hitCount / total;
    }

    /**
     * Get cache statistics as a string.
     * @return formatted statistics
     */
    public String getStats() {
        return String.format(
            "CacheStats{size=%d, hits=%d, misses=%d, hitRate=%.2f%%}",
            size(), hitCount, missCount, getHitRate() * 100
        );
    }

    /**
     * Shuts down the cleanup executor if running.
     * Call this when the cache is no longer needed.
     */
    public void shutdown() {
        if (cleanupExecutor != null) {
            cleanupExecutor.shutdown();
        }
    }

    /**
     * Refresh a cached value with a new TTL.
     * @param key cache key
     * @param ttlMillis new TTL in milliseconds
     * @return true if the entry was refreshed
     */
    @SuppressWarnings("unchecked")
    public <T> boolean refreshTtl(String key, long ttlMillis) {
        CacheEntry<?> entry = cache.get(key);
        if (entry == null || entry.isExpired()) {
            return false;
        }
        cache.put(key, new CacheEntry<>((T) entry.value, ttlMillis));
        return true;
    }

    /**
     * Put a value that never expires.
     * @param key cache key
     * @param value value to store
     * @param <T> value type
     */
    public <T> void putPermanent(String key, T value) {
        put(key, value, Long.MAX_VALUE);
    }

    /**
     * Get all keys in the cache (including expired ones until cleanup).
     * @return array of keys
     */
    public String[] keys() {
        return cache.keySet().toArray(new String[0]);
    }

    // Private helper method to enforce max size
    private void enforceMaxSize() {
        if (maxSize <= 0) return;
        
        while (cache.size() >= maxSize) {
            // Simple eviction: remove a random entry
            String keyToRemove = cache.keySet().iterator().next();
            cache.remove(keyToRemove);
        }
    }

    // Static utility methods

    /**
     * Create a simple cache with default settings.
     * @return new CacheUtils instance
     */
    public static CacheUtils create() {
        return new CacheUtils();
    }

    /**
     * Create a cache with specified TTL.
     * @param ttlMillis default TTL in milliseconds
     * @return new CacheUtils instance
     */
    public static CacheUtils withTtl(long ttlMillis) {
        return new CacheUtils(ttlMillis);
    }

    /**
     * Create a cache with specified TTL.
     * @param ttl default TTL duration
     * @return new CacheUtils instance
     */
    public static CacheUtils withTtl(Duration ttl) {
        return new CacheUtils(ttl.toMillis());
    }

    /**
     * Create a cache with max size limit.
     * @param maxSize maximum number of entries
     * @return new CacheUtils instance
     */
    public static CacheUtils withMaxSize(int maxSize) {
        return builder().maxSize(maxSize).build();
    }

    /**
     * Create a cache with background cleanup.
     * @param ttlMillis default TTL
     * @param cleanupIntervalMillis cleanup interval
     * @return new CacheUtils instance
     */
    public static CacheUtils withCleanup(long ttlMillis, long cleanupIntervalMillis) {
        return builder()
            .defaultTtlMillis(ttlMillis)
            .enableCleanup(cleanupIntervalMillis)
            .build();
    }
}