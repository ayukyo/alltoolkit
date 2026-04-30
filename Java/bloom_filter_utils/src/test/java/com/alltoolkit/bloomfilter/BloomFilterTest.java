package com.alltoolkit.bloomfilter;

import org.junit.Test;
import static org.junit.Assert.*;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Unit tests for BloomFilter implementation
 */
public class BloomFilterTest {
    
    @Test
    public void testBloomConfigOptimal() {
        BloomFilter.BloomConfig config = BloomFilter.BloomConfig.optimal(1000, 0.01);
        assertTrue("Size should be positive", config.getSize() > 0);
        assertTrue("Hash count should be positive", config.getHashCount() > 0);
        assertTrue("Hash count should be <= 32", config.getHashCount() <= 32);
    }
    
    @Test
    public void testBloomFilterBasicString() {
        BloomFilter<String> filter = new BloomFilter<>(BloomFilter.stringSerializer());
        
        filter.insert("hello");
        filter.insert("world");
        
        assertTrue("Should contain 'hello'", filter.contains("hello"));
        assertTrue("Should contain 'world'", filter.contains("world"));
        assertFalse("Should not contain 'missing'", filter.contains("missing"));
    }
    
    @Test
    public void testBloomFilterBasicInteger() {
        BloomFilter<Integer> filter = new BloomFilter<>(BloomFilter.intSerializer());
        
        for (int i = 0; i < 100; i++) {
            filter.insert(i);
        }
        
        for (int i = 0; i < 100; i++) {
            assertTrue("Should contain " + i, filter.contains(i));
        }
        
        // Check some missing values
        int falsePositives = 0;
        for (int i = 100; i < 200; i++) {
            if (filter.contains(i)) {
                falsePositives++;
            }
        }
        
        // False positive rate should be low
        double actualRate = falsePositives / 100.0;
        System.out.println("Integer filter - False positive rate: " + actualRate);
        assertTrue("False positive rate should be reasonable", actualRate < 0.1);
    }
    
    @Test
    public void testBloomFilterWithRate() {
        BloomFilter<Integer> filter = new BloomFilter<>(1000, 0.01, BloomFilter.intSerializer());
        
        for (int i = 0; i < 1000; i++) {
            filter.insert(i);
        }
        
        // All inserted items should be found
        for (int i = 0; i < 1000; i++) {
            assertTrue("Should contain " + i, filter.contains(i));
        }
        
        // Check false positive rate
        int falsePositives = 0;
        int testCount = 10000;
        for (int i = 1000; i < 1000 + testCount; i++) {
            if (filter.contains(i)) {
                falsePositives++;
            }
        }
        
        double actualRate = falsePositives / (double) testCount;
        System.out.println("Actual false positive rate: " + actualRate);
        assertTrue("False positive rate should be < 5%", actualRate < 0.05);
    }
    
    @Test
    public void testBloomFilterClear() {
        BloomFilter<String> filter = new BloomFilter<>(BloomFilter.stringSerializer());
        
        filter.insert("test");
        assertTrue("Should contain 'test'", filter.contains("test"));
        
        filter.clear();
        assertFalse("Should not contain 'test' after clear", filter.contains("test"));
        assertTrue("Should be empty", filter.isEmpty());
    }
    
    @Test
    public void testBloomFilterCheckAndInsert() {
        BloomFilter<String> filter = new BloomFilter<>(BloomFilter.stringSerializer());
        
        assertFalse("First check should return false", filter.checkAndInsert("first"));
        assertTrue("Second check should return true", filter.checkAndInsert("first"));
        assertFalse("New item should return false", filter.checkAndInsert("second"));
        assertTrue("Second item now present", filter.checkAndInsert("second"));
    }
    
    @Test
    public void testBloomFilterMerge() {
        BloomFilter.BloomConfig config = BloomFilter.BloomConfig.optimal(100, 0.01);
        BloomFilter<Integer> filter1 = new BloomFilter<>(config, BloomFilter.intSerializer());
        BloomFilter<Integer> filter2 = new BloomFilter<>(config, BloomFilter.intSerializer());
        
        for (int i = 0; i < 50; i++) {
            filter1.insert(i);
        }
        for (int i = 50; i < 100; i++) {
            filter2.insert(i);
        }
        
        filter1.merge(filter2);
        
        // All items should be found in merged filter
        for (int i = 0; i < 100; i++) {
            assertTrue("Merged filter should contain " + i, filter1.contains(i));
        }
    }
    
    @Test
    public void testBloomFilterSerialization() throws IOException {
        BloomFilter<String> filter = new BloomFilter<>(100, 0.01, BloomFilter.stringSerializer());
        
        filter.insert("apple");
        filter.insert("banana");
        filter.insert("cherry");
        
        byte[] bytes = filter.toBytes();
        BloomFilter<String> restored = BloomFilter.fromBytes(bytes, BloomFilter.stringSerializer());
        
        assertTrue("Restored should contain 'apple'", restored.contains("apple"));
        assertTrue("Restored should contain 'banana'", restored.contains("banana"));
        assertTrue("Restored should contain 'cherry'", restored.contains("cherry"));
        assertFalse("Restored should not contain 'missing'", restored.contains("missing"));
        assertEquals("Size should match", filter.size(), restored.size());
    }
    
    @Test
    public void testBloomFilterFillRatio() {
        BloomFilter<Integer> filter = new BloomFilter<>(100, 0.1, BloomFilter.intSerializer());
        
        double initialRatio = filter.fillRatio();
        assertEquals("Initial fill ratio should be 0", 0.0, initialRatio, 0.001);
        
        for (int i = 0; i < 50; i++) {
            filter.insert(i);
        }
        
        double filledRatio = filter.fillRatio();
        System.out.println("Fill ratio after 50 items: " + filledRatio);
        assertTrue("Fill ratio should increase", filledRatio > 0.0);
        assertTrue("Fill ratio should be < 1", filledRatio < 1.0);
    }
    
    @Test
    public void testBloomFilterEmpty() {
        BloomFilter<String> filter = new BloomFilter<>(BloomFilter.stringSerializer());
        assertTrue("New filter should be empty", filter.isEmpty());
        assertEquals("New filter size should be 0", 0, filter.size());
    }
    
    @Test
    public void testBloomFilterLargeDataset() {
        BloomFilter<Integer> filter = new BloomFilter<>(100000, 0.01, BloomFilter.intSerializer());
        
        int numItems = 50000;
        for (int i = 0; i < numItems; i++) {
            filter.insert(i);
        }
        
        // Verify all items are found
        for (int i = 0; i < numItems; i += 1000) {
            assertTrue("Should contain " + i, filter.contains(i));
        }
        
        // Check false positive rate
        int falsePositives = 0;
        int testCount = 10000;
        for (int i = numItems; i < numItems + testCount; i++) {
            if (filter.contains(i)) {
                falsePositives++;
            }
        }
        
        double actualRate = falsePositives / (double) testCount;
        System.out.println("Large dataset - False positive rate: " + actualRate);
        assertTrue("False positive rate should be < 5%", actualRate < 0.05);
    }
}