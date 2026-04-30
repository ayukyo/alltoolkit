package com.alltoolkit.bloomfilter;

import org.junit.Test;
import static org.junit.Assert.*;

import java.io.IOException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Unit tests for ConcurrentBloomFilter implementation
 */
public class ConcurrentBloomFilterTest {
    
    @Test
    public void testConcurrentBloomFilterBasic() {
        ConcurrentBloomFilter<String> filter = new ConcurrentBloomFilter<>(
                BloomFilter.stringSerializer());
        
        filter.insert("hello");
        filter.insert("world");
        
        assertTrue("Should contain 'hello'", filter.contains("hello"));
        assertTrue("Should contain 'world'", filter.contains("world"));
        assertFalse("Should not contain 'missing'", filter.contains("missing"));
    }
    
    @Test
    public void testConcurrentBloomFilterWithRate() {
        ConcurrentBloomFilter<Integer> filter = new ConcurrentBloomFilter<>(
                1000, 0.01, BloomFilter.intSerializer());
        
        for (int i = 0; i < 1000; i++) {
            filter.insert(i);
        }
        
        // All inserted items should be found
        for (int i = 0; i < 1000; i++) {
            assertTrue("Should contain " + i, filter.contains(i));
        }
    }
    
    @Test
    public void testConcurrentBloomFilterSerialization() throws IOException {
        ConcurrentBloomFilter<String> filter = new ConcurrentBloomFilter<>(
                100, 0.01, BloomFilter.stringSerializer());
        
        filter.insert("apple");
        filter.insert("banana");
        
        byte[] bytes = filter.toBytes();
        ConcurrentBloomFilter<String> restored = ConcurrentBloomFilter.fromBytes(
                bytes, BloomFilter.stringSerializer());
        
        assertTrue("Restored should contain 'apple'", restored.contains("apple"));
        assertTrue("Restored should contain 'banana'", restored.contains("banana"));
        assertEquals("Size should match", filter.size(), restored.size());
    }
    
    @Test
    public void testConcurrentAccess() throws InterruptedException {
        final ConcurrentBloomFilter<Integer> filter = new ConcurrentBloomFilter<>(
                10000, 0.01, BloomFilter.intSerializer());
        
        int numThreads = 10;
        int itemsPerThread = 1000;
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        CountDownLatch startLatch = new CountDownLatch(1);
        CountDownLatch endLatch = new CountDownLatch(numThreads);
        AtomicInteger errors = new AtomicInteger(0);
        
        // Submit tasks
        for (int t = 0; t < numThreads; t++) {
            final int threadId = t;
            executor.submit(() -> {
                try {
                    startLatch.await();
                    
                    // Insert items
                    for (int i = 0; i < itemsPerThread; i++) {
                        int item = threadId * itemsPerThread + i;
                        filter.insert(item);
                    }
                    
                    // Verify items
                    for (int i = 0; i < itemsPerThread; i++) {
                        int item = threadId * itemsPerThread + i;
                        if (!filter.contains(item)) {
                            errors.incrementAndGet();
                        }
                    }
                    
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    endLatch.countDown();
                }
            });
        }
        
        // Start all threads simultaneously
        startLatch.countDown();
        
        // Wait for completion
        endLatch.await();
        executor.shutdown();
        
        assertEquals("No errors should occur during concurrent access", 0, errors.get());
        assertEquals("Total items should match", numThreads * itemsPerThread, filter.size());
        
        System.out.println("Concurrent test passed: " + filter.size() + " items inserted");
    }
    
    @Test
    public void testConcurrentBloomFilterClear() {
        ConcurrentBloomFilter<String> filter = new ConcurrentBloomFilter<>(
                BloomFilter.stringSerializer());
        
        filter.insert("test");
        assertTrue("Should contain 'test'", filter.contains("test"));
        
        filter.clear();
        assertFalse("Should not contain 'test' after clear", filter.contains("test"));
        assertTrue("Should be empty", filter.isEmpty());
    }
    
    @Test
    public void testConcurrentBloomFilterStatistics() {
        ConcurrentBloomFilter<Integer> filter = new ConcurrentBloomFilter<>(
                100, 0.1, BloomFilter.intSerializer());
        
        assertTrue("Should be empty initially", filter.isEmpty());
        assertEquals("Initial size should be 0", 0, filter.size());
        assertEquals("Initial bit count should be 0", 0, filter.bitCount());
        
        for (int i = 0; i < 50; i++) {
            filter.insert(i);
        }
        
        assertFalse("Should not be empty", filter.isEmpty());
        assertEquals("Size should be 50", 50, filter.size());
        assertTrue("Bit count should be > 0", filter.bitCount() > 0);
        assertTrue("Fill ratio should be > 0", filter.fillRatio() > 0);
        assertTrue("False positive rate should be > 0", filter.currentFalsePositiveRate() > 0);
    }
}