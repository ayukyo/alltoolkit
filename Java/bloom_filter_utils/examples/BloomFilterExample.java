package com.alltoolkit.bloomfilter.examples;

import com.alltoolkit.bloomfilter.*;

/**
 * Example usage of Bloom Filter utilities
 * 
 * This example demonstrates:
 * 1. Basic Bloom filter operations
 * 2. Optimal configuration
 * 3. Scalable Bloom filter
 * 4. Thread-safe concurrent access
 * 5. Serialization for persistence
 */
public class BloomFilterExample {
    
    public static void main(String[] args) throws Exception {
        System.out.println("=== Bloom Filter Examples ===\n");
        
        // Example 1: Basic String Bloom Filter
        basicStringExample();
        
        // Example 2: Integer Bloom Filter with Optimal Config
        optimalConfigExample();
        
        // Example 3: False Positive Rate Analysis
        falsePositiveAnalysis();
        
        // Example 4: Scalable Bloom Filter
        scalableBloomFilterExample();
        
        // Example 5: Concurrent Bloom Filter
        concurrentBloomFilterExample();
        
        // Example 6: Serialization
        serializationExample();
        
        // Example 7: URL Deduplication Use Case
        urlDeduplicationExample();
        
        // Example 8: Username Check Use Case
        usernameCheckExample();
    }
    
    /**
     * Example 1: Basic String Bloom Filter
     */
    private static void basicStringExample() {
        System.out.println("--- Example 1: Basic String Bloom Filter ---");
        
        // Create a Bloom filter for Strings with default settings
        BloomFilter<String> filter = new BloomFilter<>(BloomFilter.stringSerializer());
        
        // Add some words
        filter.insert("apple");
        filter.insert("banana");
        filter.insert("cherry");
        filter.insert("date");
        filter.insert("elderberry");
        
        System.out.println("Filter info: " + filter);
        
        // Check membership
        String[] testWords = {"apple", "banana", "fig", "grape", "elderberry"};
        for (String word : testWords) {
            boolean exists = filter.contains(word);
            System.out.println("  '" + word + "': " + (exists ? "probably exists" : "definitely not in set"));
        }
        
        System.out.println();
    }
    
    /**
     * Example 2: Integer Bloom Filter with Optimal Config
     */
    private static void optimalConfigExample() {
        System.out.println("--- Example 2: Optimal Configuration ---");
        
        // Create optimal config for 10000 items with 1% false positive rate
        BloomFilter.BloomConfig config = BloomFilter.BloomConfig.optimal(10000, 0.01);
        System.out.println("Optimal config for 10000 items, 1% FPR:");
        System.out.println("  Size: " + config.getSize() + " bits");
        System.out.println("  Hash functions: " + config.getHashCount());
        
        // Create filter with this config
        BloomFilter<Integer> filter = new BloomFilter<>(config, BloomFilter.intSerializer());
        
        // Add some integers
        for (int i = 0; i < 5000; i++) {
            filter.insert(i);
        }
        
        System.out.println("\nAfter inserting 5000 items:");
        System.out.println("  Items: " + filter.size());
        System.out.println("  Bits set: " + filter.bitCount());
        System.out.println("  Fill ratio: " + String.format("%.4f", filter.fillRatio()));
        System.out.println("  Estimated FPR: " + String.format("%.6f", filter.currentFalsePositiveRate()));
        
        System.out.println();
    }
    
    /**
     * Example 3: False Positive Rate Analysis
     */
    private static void falsePositiveAnalysis() {
        System.out.println("--- Example 3: False Positive Rate Analysis ---");
        
        int expectedItems = 1000;
        double targetFPR = 0.01; // 1%
        
        BloomFilter<Integer> filter = new BloomFilter<>(
                expectedItems, targetFPR, BloomFilter.intSerializer());
        
        // Insert items
        for (int i = 0; i < expectedItems; i++) {
            filter.insert(i);
        }
        
        // Measure actual false positive rate
        int falsePositives = 0;
        int testCount = 10000;
        for (int i = expectedItems; i < expectedItems + testCount; i++) {
            if (filter.contains(i)) {
                falsePositives++;
            }
        }
        
        double actualFPR = falsePositives / (double) testCount;
        System.out.println("Target FPR: " + (targetFPR * 100) + "%");
        System.out.println("Actual FPR: " + String.format("%.4f", actualFPR * 100) + "%");
        System.out.println("False positives found: " + falsePositives + " out of " + testCount);
        
        System.out.println();
    }
    
    /**
     * Example 4: Scalable Bloom Filter
     */
    private static void scalableBloomFilterExample() {
        System.out.println("--- Example 4: Scalable Bloom Filter ---");
        
        ScalableBloomFilter<String> filter = new ScalableBloomFilter<>(
                100, 0.01, BloomFilter.stringSerializer());
        
        System.out.println("Initial filter count: " + filter.filterCount());
        
        // Insert many items - filter will grow automatically
        int numItems = 10000;
        for (int i = 0; i < numItems; i++) {
            filter.insert("user_" + i);
        }
        
        System.out.println("After inserting " + numItems + " items:");
        System.out.println("  Filter count: " + filter.filterCount());
        System.out.println("  Total items: " + filter.size());
        System.out.println("  Estimated FPR: " + String.format("%.6f", filter.estimatedFalsePositiveRate()));
        
        // Verify some items
        System.out.println("\nSample membership tests:");
        String[] tests = {"user_0", "user_5000", "user_9999", "user_10000", "unknown"};
        for (String test : tests) {
            System.out.println("  '" + test + "': " + filter.contains(test));
        }
        
        System.out.println();
    }
    
    /**
     * Example 5: Concurrent Bloom Filter
     */
    private static void concurrentBloomFilterExample() throws InterruptedException {
        System.out.println("--- Example 5: Concurrent Bloom Filter ---");
        
        ConcurrentBloomFilter<Integer> filter = new ConcurrentBloomFilter<>(
                100000, 0.01, BloomFilter.intSerializer());
        
        int numThreads = 4;
        int itemsPerThread = 10000;
        Thread[] threads = new Thread[numThreads];
        
        // Create threads that insert items concurrently
        for (int t = 0; t < numThreads; t++) {
            final int threadId = t;
            threads[t] = new Thread(() -> {
                for (int i = 0; i < itemsPerThread; i++) {
                    int item = threadId * itemsPerThread + i;
                    filter.insert(item);
                }
            });
        }
        
        // Start all threads
        long startTime = System.currentTimeMillis();
        for (Thread thread : threads) {
            thread.start();
        }
        
        // Wait for completion
        for (Thread thread : threads) {
            thread.join();
        }
        long duration = System.currentTimeMillis() - startTime;
        
        System.out.println("Concurrent insertion completed:");
        System.out.println("  Threads: " + numThreads);
        System.out.println("  Items per thread: " + itemsPerThread);
        System.out.println("  Total items: " + filter.size());
        System.out.println("  Time: " + duration + "ms");
        
        System.out.println();
    }
    
    /**
     * Example 6: Serialization
     */
    private static void serializationExample() throws Exception {
        System.out.println("--- Example 6: Serialization ---");
        
        // Create and populate filter
        BloomFilter<String> original = new BloomFilter<>(
                1000, 0.01, BloomFilter.stringSerializer());
        
        String[] words = {"alpha", "beta", "gamma", "delta", "epsilon"};
        for (String word : words) {
            original.insert(word);
        }
        
        System.out.println("Original filter: " + original);
        
        // Serialize to bytes
        byte[] bytes = original.toBytes();
        System.out.println("Serialized size: " + bytes.length + " bytes");
        
        // Deserialize
        BloomFilter<String> restored = BloomFilter.fromBytes(bytes, BloomFilter.stringSerializer());
        System.out.println("Restored filter: " + restored);
        
        // Verify data integrity
        System.out.println("\nMembership verification after restore:");
        for (String word : words) {
            boolean inOriginal = original.contains(word);
            boolean inRestored = restored.contains(word);
            System.out.println("  '" + word + "': original=" + inOriginal + ", restored=" + inRestored);
        }
        
        System.out.println();
    }
    
    /**
     * Example 7: URL Deduplication Use Case
     */
    private static void urlDeduplicationExample() {
        System.out.println("--- Example 7: URL Deduplication ---");
        
        // Bloom filter for URL deduplication
        BloomFilter<String> visitedUrls = new BloomFilter<>(
                100000, 0.001, // 100K URLs, 0.1% false positive rate
                BloomFilter.stringSerializer());
        
        // Simulate crawling URLs
        String[] urls = {
            "https://example.com/page1",
            "https://example.com/page2",
            "https://example.com/page3",
            "https://example.com/page1", // duplicate
            "https://example.com/page4",
            "https://example.com/page2", // duplicate
        };
        
        int newUrls = 0;
        int skipped = 0;
        
        for (String url : urls) {
            if (visitedUrls.contains(url)) {
                System.out.println("  SKIP (already visited): " + url);
                skipped++;
            } else {
                visitedUrls.insert(url);
                System.out.println("  NEW: " + url);
                newUrls++;
            }
        }
        
        System.out.println("\nSummary:");
        System.out.println("  New URLs visited: " + newUrls);
        System.out.println("  Duplicates skipped: " + skipped);
        System.out.println("  Filter info: " + visitedUrls);
        
        System.out.println();
    }
    
    /**
     * Example 8: Username Check Use Case
     */
    private static void usernameCheckExample() {
        System.out.println("--- Example 8: Username Availability Check ---");
        
        // Scalable Bloom filter for usernames (grows as needed)
        ScalableBloomFilter<String> takenUsernames = new ScalableBloomFilter<>(
                1000, 0.001, // 1000 initial capacity, 0.1% FPR
                BloomFilter.stringSerializer());
        
        // Pre-populate with existing usernames
        String[] existing = {"alice", "bob", "charlie", "david", "eve"};
        for (String name : existing) {
            takenUsernames.insert(name);
        }
        
        System.out.println("Existing usernames registered.");
        
        // Check availability of new usernames
        String[] requests = {"alice", "frank", "grace", "bob", "henry"};
        
        for (String name : requests) {
            boolean mightBeTaken = takenUsernames.contains(name);
            if (mightBeTaken) {
                System.out.println("  '" + name + "': LIKELY TAKEN (may be false positive)");
            } else {
                System.out.println("  '" + name + "': AVAILABLE (definitely not taken)");
                takenUsernames.insert(name);
            }
        }
        
        System.out.println("\nFilter stats: " + takenUsernames);
        
        System.out.println();
    }
}