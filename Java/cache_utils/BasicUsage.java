// Basic usage examples for CacheUtils

import java.time.Duration;
import java.util.Optional;

/**
 * Basic usage examples for CacheUtils.
 */
public class BasicUsage {

    public static void main(String[] args) throws InterruptedException {
        // ===========================================
        // Example 1: Simple Cache
        // ===========================================
        System.out.println("=== Example 1: Simple Cache ===");
        
        CacheUtils cache = new CacheUtils();
        
        // Store values
        cache.put("name", "Alice");
        cache.put("age", 30);
        cache.put("active", true);
        
        // Retrieve values
        Optional<String> name = cache.get("name");
        Optional<Integer> age = cache.get("age");
        Optional<Boolean> active = cache.get("active");
        
        System.out.println("Name: " + name.orElse("Unknown"));
        System.out.println("Age: " + age.orElse(0));
        System.out.println("Active: " + active.orElse(false));
        
        // Check existence
        System.out.println("Has 'name': " + cache.contains("name"));
        System.out.println("Has 'email': " + cache.contains("email"));
        
        System.out.println();
        
        // ===========================================
        // Example 2: TTL (Time-To-Live)
        // ===========================================
        System.out.println("=== Example 2: TTL ===");
        
        CacheUtils ttlCache = new CacheUtils(2000); // 2 second default TTL
        
        ttlCache.put("session1", "user123");
        ttlCache.put("session2", "user456", 500); // 500ms TTL
        ttlCache.putPermanent("config", "production");
        
        System.out.println("Immediately after put:");
        System.out.println("  session1: " + ttlCache.get("session1").orElse("expired"));
        System.out.println("  session2: " + ttlCache.get("session2").orElse("expired"));
        
        Thread.sleep(600);
        
        System.out.println("After 600ms:");
        System.out.println("  session1: " + ttlCache.get("session1").orElse("expired"));
        System.out.println("  session2: " + ttlCache.get("session2").orElse("expired")); // Expired
        System.out.println("  config: " + ttlCache.get("config").orElse("expired")); // Still there
        
        ttlCache.shutdown();
        System.out.println();
        
        // ===========================================
        // Example 3: Get-Or-Compute Pattern
        // ===========================================
        System.out.println("=== Example 3: Get-Or-Compute ===");
        
        CacheUtils computeCache = new CacheUtils(Duration.ofMinutes(5).toMillis());
        
        // First call computes
        String data1 = computeCache.getOrCompute("expensive-data", () -> {
            System.out.println("  Computing expensive data...");
            return "computed-result";
        });
        System.out.println("First call: " + data1);
        
        // Second call uses cache
        String data2 = computeCache.getOrCompute("expensive-data", () -> {
            System.out.println("  This won't print!");
            return "should-not-appear";
        });
        System.out.println("Second call: " + data2);
        
        System.out.println();
        
        // ===========================================
        // Example 4: Builder Pattern
        // ===========================================
        System.out.println("=== Example 4: Builder Pattern ===");
        
        CacheUtils builtCache = CacheUtils.builder()
            .defaultTtl(Duration.ofMinutes(10))
            .maxSize(100)
            .enableCleanup(Duration.ofSeconds(30).toMillis())
            .build();
        
        builtCache.put("key1", "value1");
        builtCache.put("key2", "value2");
        
        System.out.println("Cache size: " + builtCache.size());
        System.out.println("Stats: " + builtCache.getStats());
        
        builtCache.shutdown();
        System.out.println();
        
        // ===========================================
        // Example 5: Cache Statistics
        // ===========================================
        System.out.println("=== Example 5: Statistics ===");
        
        CacheUtils statsCache = new CacheUtils();
        
        statsCache.put("a", "1");
        statsCache.put("b", "2");
        
        // Hits
        statsCache.get("a");
        statsCache.get("a");
        statsCache.get("b");
        
        // Misses
        statsCache.get("x");
        statsCache.get("y");
        statsCache.get("z");
        
        System.out.println("Hits: " + statsCache.getHitCount());
        System.out.println("Misses: " + statsCache.getMissCount());
        System.out.println("Hit Rate: " + String.format("%.2f%%", statsCache.getHitRate() * 100));
        System.out.println("Full Stats: " + statsCache.getStats());
        System.out.println();
        
        // ===========================================
        // Example 6: Cleanup and Shutdown
        // ===========================================
        System.out.println("=== Example 6: Cleanup ===");
        
        CacheUtils cleanupCache = CacheUtils.builder()
            .defaultTtlMillis(100)
            .enableCleanup(50)
            .build();
        
        cleanupCache.put("temp1", "data1");
        cleanupCache.put("temp2", "data2");
        cleanupCache.putPermanent("permanent", "forever");
        
        System.out.println("Before cleanup: " + cleanupCache.size() + " entries");
        
        Thread.sleep(200); // Wait for expiration
        
        System.out.println("After expiration: " + cleanupCache.size() + " entries");
        System.out.println("Permanent entry: " + cleanupCache.get("permanent").orElse("gone"));
        
        // Manual cleanup
        cleanupCache.cleanupExpired();
        
        // Clear all
        cleanupCache.clear();
        System.out.println("After clear: " + cleanupCache.size() + " entries");
        
        cleanupCache.shutdown();
        System.out.println();
        
        // ===========================================
        // Example 7: Static Factory Methods
        // ===========================================
        System.out.println("=== Example 7: Static Factories ===");
        
        // Simple cache
        CacheUtils simple = CacheUtils.create();
        simple.put("key", "value");
        System.out.println("Simple: " + simple.get("key").orElse("none"));
        simple.shutdown();
        
        // With TTL
        CacheUtils withTtl = CacheUtils.withTtl(1000);
        withTtl.put("key", "value");
        System.out.println("With TTL: " + withTtl.get("key").orElse("none"));
        withTtl.shutdown();
        
        // With Duration
        CacheUtils withDuration = CacheUtils.withTtl(Duration.ofMinutes(5));
        withDuration.put("key", "value");
        System.out.println("With Duration: " + withDuration.get("key").orElse("none"));
        withDuration.shutdown();
        
        // With max size
        CacheUtils limited = CacheUtils.withMaxSize(3);
        limited.put("a", "1");
        limited.put("b", "2");
        limited.put("c", "3");
        limited.put("d", "4"); // Will evict one
        System.out.println("Limited size: " + limited.size());
        limited.shutdown();
        
        System.out.println();
        System.out.println("=== All Examples Complete ===");
    }
}