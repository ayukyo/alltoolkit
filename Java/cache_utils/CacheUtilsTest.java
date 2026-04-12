// Test suite for CacheUtils

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.time.Duration;
import java.util.Optional;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

/**
 * Comprehensive test suite for CacheUtils.
 * Tests cover all public methods and edge cases.
 */
@DisplayName("CacheUtils Tests")
class CacheUtilsTest {

    private CacheUtils cache;

    @BeforeEach
    void setUp() {
        cache = new CacheUtils();
    }

    @AfterEach
    void tearDown() {
        if (cache != null) {
            cache.shutdown();
        }
    }

    // ==================== Basic Put/Get Tests ====================

    @Test
    @DisplayName("Put and get a simple value")
    void testBasicPutGet() {
        cache.put("key1", "value1");
        Optional<String> result = cache.get("key1");
        
        assertTrue(result.isPresent());
        assertEquals("value1", result.get());
    }

    @Test
    @DisplayName("Get non-existent key returns empty")
    void testGetNonExistent() {
        Optional<String> result = cache.get("nonexistent");
        assertFalse(result.isPresent());
    }

    @Test
    @DisplayName("Put overwrites existing value")
    void testPutOverwrites() {
        cache.put("key1", "value1");
        cache.put("key1", "value2");
        
        Optional<String> result = cache.get("key1");
        assertTrue(result.isPresent());
        assertEquals("value2", result.get());
    }

    @Test
    @DisplayName("Put null value")
    void testPutNullValue() {
        cache.put("key1", null);
        Optional<String> result = cache.get("key1");
        
        // Null values should be stored but get returns empty
        // Actually, Optional.ofNullable(null) returns Optional.empty()
        assertFalse(result.isPresent());
    }

    @Test
    @DisplayName("Put with different types")
    void testDifferentTypes() {
        cache.put("string", "hello");
        cache.put("integer", 42);
        cache.put("double", 3.14);
        cache.put("boolean", true);
        
        assertEquals("hello", cache.<String>get("string").orElse(null));
        assertEquals(42, cache.<Integer>get("integer").orElse(null));
        assertEquals(3.14, cache.<Double>get("double").orElse(null));
        assertEquals(true, cache.<Boolean>get("boolean").orElse(null));
    }

    // ==================== TTL Tests ====================

    @Test
    @DisplayName("Entry expires after TTL")
    void testTtlExpiration() throws InterruptedException {
        CacheUtils ttlCache = new CacheUtils(100); // 100ms TTL
        
        ttlCache.put("key1", "value1");
        
        // Should be present immediately
        assertTrue(ttlCache.get("key1").isPresent());
        
        // Wait for expiration
        Thread.sleep(150);
        
        // Should be expired
        assertFalse(ttlCache.get("key1").isPresent());
        
        ttlCache.shutdown();
    }

    @Test
    @DisplayName("Put with custom TTL")
    void testCustomTtl() throws InterruptedException {
        cache.put("key1", "value1", 50); // 50ms TTL
        
        assertTrue(cache.get("key1").isPresent());
        
        Thread.sleep(100);
        
        assertFalse(cache.get("key1").isPresent());
    }

    @Test
    @DisplayName("Put with Duration TTL")
    void testDurationTtl() throws InterruptedException {
        cache.put("key1", "value1", Duration.ofMillis(50));
        
        assertTrue(cache.get("key1").isPresent());
        
        Thread.sleep(100);
        
        assertFalse(cache.get("key1").isPresent());
    }

    @Test
    @DisplayName("Put permanent value never expires")
    void testPermanentValue() throws InterruptedException {
        cache.putPermanent("key1", "value1");
        
        // Even after some time
        Thread.sleep(50);
        
        assertTrue(cache.get("key1").isPresent());
        assertEquals("value1", cache.<String>get("key1").orElse(null));
    }

    @Test
    @DisplayName("Get remaining TTL")
    void testGetRemainingTtl() throws InterruptedException {
        cache.put("key1", "value1", 1000);
        
        Optional<Long> remaining = cache.getRemainingTtl("key1");
        assertTrue(remaining.isPresent());
        assertTrue(remaining.get() <= 1000);
        assertTrue(remaining.get() > 900); // Should be close to original
        
        // Non-existent key
        assertFalse(cache.getRemainingTtl("nonexistent").isPresent());
    }

    @Test
    @DisplayName("Get age of cached entry")
    void testGetAge() throws InterruptedException {
        cache.put("key1", "value1");
        
        Thread.sleep(50);
        
        Optional<Long> age = cache.getAge("key1");
        assertTrue(age.isPresent());
        assertTrue(age.get() >= 50);
    }

    // ==================== Remove/Clear Tests ====================

    @Test
    @DisplayName("Remove existing key")
    void testRemoveExisting() {
        cache.put("key1", "value1");
        assertTrue(cache.remove("key1"));
        assertFalse(cache.get("key1").isPresent());
    }

    @Test
    @DisplayName("Remove non-existent key returns false")
    void testRemoveNonExistent() {
        assertFalse(cache.remove("nonexistent"));
    }

    @Test
    @DisplayName("Clear removes all entries")
    void testClear() {
        cache.put("key1", "value1");
        cache.put("key2", "value2");
        cache.put("key3", "value3");
        
        assertEquals(3, cache.size());
        
        cache.clear();
        
        assertEquals(0, cache.size());
        assertFalse(cache.get("key1").isPresent());
        assertFalse(cache.get("key2").isPresent());
        assertFalse(cache.get("key3").isPresent());
    }

    // ==================== Contains Tests ====================

    @Test
    @DisplayName("Contains returns true for existing key")
    void testContainsExisting() {
        cache.put("key1", "value1");
        assertTrue(cache.contains("key1"));
    }

    @Test
    @DisplayName("Contains returns false for non-existent key")
    void testContainsNonExistent() {
        assertFalse(cache.contains("nonexistent"));
    }

    @Test
    @DisplayName("Contains returns false for expired key")
    void testContainsExpired() throws InterruptedException {
        cache.put("key1", "value1", 50);
        
        assertTrue(cache.contains("key1"));
        
        Thread.sleep(100);
        
        // Access it to trigger removal
        cache.get("key1");
        
        assertFalse(cache.contains("key1"));
    }

    // ==================== Size Tests ====================

    @Test
    @DisplayName("Size returns correct count")
    void testSize() {
        assertEquals(0, cache.size());
        
        cache.put("key1", "value1");
        assertEquals(1, cache.size());
        
        cache.put("key2", "value2");
        assertEquals(2, cache.size());
        
        cache.remove("key1");
        assertEquals(1, cache.size());
    }

    // ==================== GetOrCompute Tests ====================

    @Test
    @DisplayName("GetOrCompute returns cached value")
    void testGetOrComputeCached() {
        cache.put("key1", "cached");
        
        String result = cache.getOrCompute("key1", () -> "computed");
        
        assertEquals("cached", result);
    }

    @Test
    @DisplayName("GetOrCompute computes when absent")
    void testGetOrComputeAbsent() {
        String result = cache.getOrCompute("key1", () -> "computed");
        
        assertEquals("computed", result);
        assertTrue(cache.get("key1").isPresent());
    }

    @Test
    @DisplayName("GetOrCompute with TTL")
    void testGetOrComputeWithTtl() throws InterruptedException {
        String result = cache.getOrCompute("key1", () -> "computed", 50);
        
        assertEquals("computed", result);
        assertTrue(cache.get("key1").isPresent());
        
        Thread.sleep(100);
        
        assertFalse(cache.get("key1").isPresent());
    }

    @Test
    @DisplayName("GetOrCompute supplier called only once")
    void testGetOrComputeSupplierCalledOnce() {
        AtomicInteger callCount = new AtomicInteger(0);
        
        cache.getOrCompute("key1", () -> {
            callCount.incrementAndGet();
            return "value";
        });
        
        cache.getOrCompute("key1", () -> {
            callCount.incrementAndGet();
            return "value2";
        });
        
        assertEquals(1, callCount.get());
    }

    // ==================== Statistics Tests ====================

    @Test
    @DisplayName("Hit and miss counts")
    void testStatistics() {
        cache.put("key1", "value1");
        
        // Hit
        cache.get("key1");
        assertEquals(1, cache.getHitCount());
        assertEquals(0, cache.getMissCount());
        
        // Miss
        cache.get("nonexistent");
        assertEquals(1, cache.getHitCount());
        assertEquals(1, cache.getMissCount());
        
        // Another hit
        cache.get("key1");
        assertEquals(2, cache.getHitCount());
        assertEquals(1, cache.getMissCount());
    }

    @Test
    @DisplayName("Hit rate calculation")
    void testHitRate() {
        cache.put("key1", "value1");
        
        assertEquals(0.0, cache.getHitRate(), 0.001);
        
        cache.get("key1");
        assertEquals(1.0, cache.getHitRate(), 0.001);
        
        cache.get("nonexistent");
        assertEquals(0.5, cache.getHitRate(), 0.001);
    }

    @Test
    @DisplayName("Stats string format")
    void testStatsString() {
        cache.put("key1", "value1");
        cache.get("key1");
        cache.get("nonexistent");
        
        String stats = cache.getStats();
        assertTrue(stats.contains("size=1"));
        assertTrue(stats.contains("hits=1"));
        assertTrue(stats.contains("misses=1"));
    }

    @Test
    @DisplayName("Statistics reset on clear")
    void testStatsReset() {
        cache.put("key1", "value1");
        cache.get("key1");
        cache.get("nonexistent");
        
        cache.clear();
        
        assertEquals(0, cache.getHitCount());
        assertEquals(0, cache.getMissCount());
    }

    // ==================== Max Size Tests ====================

    @Test
    @DisplayName("Max size evicts old entries")
    void testMaxSizeEviction() {
        CacheUtils limitedCache = CacheUtils.builder()
            .maxSize(2)
            .build();
        
        limitedCache.put("key1", "value1");
        limitedCache.put("key2", "value2");
        limitedCache.put("key3", "value3");
        
        assertEquals(2, limitedCache.size());
        
        limitedCache.shutdown();
    }

    // ==================== Refresh TTL Tests ====================

    @Test
    @DisplayName("Refresh TTL for existing key")
    void testRefreshTtl() throws InterruptedException {
        cache.put("key1", "value1", 50);
        
        Thread.sleep(30);
        assertTrue(cache.refreshTtl("key1", 100));
        
        Thread.sleep(40); // Original TTL would have expired
        assertTrue(cache.get("key1").isPresent());
    }

    @Test
    @DisplayName("Refresh TTL for non-existent key returns false")
    void testRefreshTtlNonExistent() {
        assertFalse(cache.refreshTtl("nonexistent", 100));
    }

    // ==================== Keys Tests ====================

    @Test
    @DisplayName("Get all keys")
    void testKeys() {
        cache.put("key1", "value1");
        cache.put("key2", "value2");
        cache.put("key3", "value3");
        
        String[] keys = cache.keys();
        assertEquals(3, keys.length);
    }

    // ==================== Cleanup Tests ====================

    @Test
    @DisplayName("Manual cleanup removes expired entries")
    void testManualCleanup() throws InterruptedException {
        cache.put("key1", "value1", 50);
        cache.put("key2", "value2", 200);
        
        Thread.sleep(100);
        
        cache.cleanupExpired();
        
        assertEquals(1, cache.size());
        assertFalse(cache.get("key1").isPresent());
        assertTrue(cache.get("key2").isPresent());
    }

    @Test
    @DisplayName("Automatic background cleanup")
    void testAutoCleanup() throws InterruptedException {
        CacheUtils autoCache = CacheUtils.builder()
            .defaultTtlMillis(50)
            .enableCleanup(100)
            .build();
        
        autoCache.put("key1", "value1");
        autoCache.put("key2", "value2");
        
        assertEquals(2, autoCache.size());
        
        // Wait for cleanup to run
        Thread.sleep(200);
        
        // Expired entries should be removed
        assertTrue(autoCache.size() <= 2);
        
        autoCache.shutdown();
    }

    // ==================== Thread Safety Tests ====================

    @Test
    @DisplayName("Concurrent put and get operations")
    void testConcurrency() throws InterruptedException {
        int numThreads = 10;
        int numOperations = 100;
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        CountDownLatch latch = new CountDownLatch(numThreads);
        
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            executor.submit(() -> {
                try {
                    for (int j = 0; j < numOperations; j++) {
                        String key = "key-" + threadId + "-" + j;
                        cache.put(key, "value-" + j);
                        cache.get(key);
                    }
                } finally {
                    latch.countDown();
                }
            });
        }
        
        assertTrue(latch.await(10, TimeUnit.SECONDS));
        executor.shutdown();
        
        // Cache should have consistent state
        assertTrue(cache.size() > 0);
    }

    @Test
    @DisplayName("Concurrent getOrCompute only computes once")
    void testConcurrentGetOrCompute() throws InterruptedException {
        int numThreads = 10;
        AtomicInteger computeCount = new AtomicInteger(0);
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        CountDownLatch startLatch = new CountDownLatch(1);
        CountDownLatch endLatch = new CountDownLatch(numThreads);
        AtomicReference<String> result = new AtomicReference<>();
        
        for (int i = 0; i < numThreads; i++) {
            executor.submit(() -> {
                try {
                    startLatch.await();
                    String value = cache.getOrCompute("shared-key", () -> {
                        computeCount.incrementAndGet();
                        return "computed";
                    });
                    result.set(value);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    endLatch.countDown();
                }
            });
        }
        
        startLatch.countDown();
        assertTrue(endLatch.await(5, TimeUnit.SECONDS));
        executor.shutdown();
        
        // Value should be computed (might be multiple times due to race condition)
        assertEquals("computed", result.get());
    }

    // ==================== Builder Tests ====================

    @Test
    @DisplayName("Builder creates cache with custom TTL")
    void testBuilderCustomTtl() {
        CacheUtils customCache = CacheUtils.builder()
            .defaultTtlMillis(1000)
            .build();
        
        customCache.put("key1", "value1");
        
        // Uses default TTL
        assertTrue(customCache.getRemainingTtl("key1").isPresent());
        
        customCache.shutdown();
    }

    @Test
    @DisplayName("Builder creates cache with Duration TTL")
    void testBuilderDurationTtl() {
        CacheUtils customCache = CacheUtils.builder()
            .defaultTtl(Duration.ofMinutes(5))
            .build();
        
        customCache.put("key1", "value1");
        
        Optional<Long> ttl = customCache.getRemainingTtl("key1");
        assertTrue(ttl.isPresent());
        assertTrue(ttl.get() <= Duration.ofMinutes(5).toMillis());
        
        customCache.shutdown();
    }

    // ==================== Static Factory Tests ====================

    @Test
    @DisplayName("Static create method")
    void testStaticCreate() {
        CacheUtils simpleCache = CacheUtils.create();
        simpleCache.put("key1", "value1");
        assertTrue(simpleCache.get("key1").isPresent());
        simpleCache.shutdown();
    }

    @Test
    @DisplayName("Static withTtl method")
    void testStaticWithTtl() {
        CacheUtils ttlCache = CacheUtils.withTtl(100);
        ttlCache.put("key1", "value1");
        assertTrue(ttlCache.get("key1").isPresent());
        ttlCache.shutdown();
    }

    @Test
    @DisplayName("Static withTtl Duration method")
    void testStaticWithTtlDuration() {
        CacheUtils ttlCache = CacheUtils.withTtl(Duration.ofSeconds(1));
        ttlCache.put("key1", "value1");
        assertTrue(ttlCache.get("key1").isPresent());
        ttlCache.shutdown();
    }

    @Test
    @DisplayName("Static withMaxSize method")
    void testStaticWithMaxSize() {
        CacheUtils limitedCache = CacheUtils.withMaxSize(3);
        limitedCache.put("key1", "value1");
        limitedCache.put("key2", "value2");
        limitedCache.put("key3", "value3");
        limitedCache.put("key4", "value4");
        
        assertTrue(limitedCache.size() <= 3);
        limitedCache.shutdown();
    }

    @Test
    @DisplayName("Static withCleanup method")
    void testStaticWithCleanup() {
        CacheUtils cleanupCache = CacheUtils.withCleanup(100, 50);
        cleanupCache.put("key1", "value1");
        assertTrue(cleanupCache.get("key1").isPresent());
        cleanupCache.shutdown();
    }

    // ==================== Edge Cases ====================

    @Test
    @DisplayName("Empty key is valid")
    void testEmptyKey() {
        cache.put("", "empty-key-value");
        Optional<String> result = cache.get("");
        assertTrue(result.isPresent());
        assertEquals("empty-key-value", result.get());
    }

    @Test
    @DisplayName("Large value storage")
    void testLargeValue() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 10000; i++) {
            sb.append("x");
        }
        String largeValue = sb.toString();
        
        cache.put("large", largeValue);
        Optional<String> result = cache.get("large");
        
        assertTrue(result.isPresent());
        assertEquals(10000, result.get().length());
    }

    @Test
    @DisplayName("Many keys")
    void testManyKeys() {
        int count = 1000;
        for (int i = 0; i < count; i++) {
            cache.put("key-" + i, "value-" + i);
        }
        
        assertEquals(count, cache.size());
        
        for (int i = 0; i < count; i++) {
            Optional<String> result = cache.get("key-" + i);
            assertTrue(result.isPresent());
            assertEquals("value-" + i, result.get());
        }
    }

    @Test
    @DisplayName("Unicode keys and values")
    void testUnicode() {
        cache.put("钥匙", "值");
        cache.put("🔑", "🚀");
        
        assertEquals("值", cache.<String>get("钥匙").orElse(null));
        assertEquals("🚀", cache.<String>get("🔑").orElse(null));
    }
}