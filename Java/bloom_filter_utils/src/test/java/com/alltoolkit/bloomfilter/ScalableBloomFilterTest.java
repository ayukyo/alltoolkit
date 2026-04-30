package com.alltoolkit.bloomfilter;

import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Unit tests for ScalableBloomFilter implementation
 */
public class ScalableBloomFilterTest {
    
    @Test
    public void testScalableBloomFilterBasic() {
        ScalableBloomFilter<String> filter = new ScalableBloomFilter<>(
                100, 0.01, BloomFilter.stringSerializer());
        
        filter.insert("hello");
        filter.insert("world");
        
        assertTrue("Should contain 'hello'", filter.contains("hello"));
        assertTrue("Should contain 'world'", filter.contains("world"));
        assertFalse("Should not contain 'missing'", filter.contains("missing"));
    }
    
    @Test
    public void testScalableBloomFilterGrowth() {
        ScalableBloomFilter<Integer> filter = new ScalableBloomFilter<>(
                100, 0.01, BloomFilter.intSerializer());
        
        assertEquals("Should start with 1 filter", 1, filter.filterCount());
        
        // Insert many items to trigger growth
        for (int i = 0; i < 10000; i++) {
            filter.insert(i);
        }
        
        // Should have grown to multiple filters
        assertTrue("Should have multiple filters", filter.filterCount() > 1);
        System.out.println("Filters created: " + filter.filterCount());
    }
    
    @Test
    public void testScalableBloomFilterLargeDataset() {
        ScalableBloomFilter<Integer> filter = new ScalableBloomFilter<>(
                1000, 0.01, BloomFilter.intSerializer());
        
        int numItems = 100000;
        for (int i = 0; i < numItems; i++) {
            filter.insert(i);
        }
        
        // All inserted items should be found
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
        System.out.println("Scalable filter - False positive rate: " + actualRate);
        System.out.println("Filters used: " + filter.filterCount());
        assertTrue("False positive rate should be reasonable", actualRate < 0.1);
    }
    
    @Test
    public void testScalableBloomFilterClear() {
        ScalableBloomFilter<String> filter = new ScalableBloomFilter<>(
                10, 0.01, BloomFilter.stringSerializer());
        
        for (int i = 0; i < 100; i++) {
            filter.insert("item" + i);
        }
        
        assertTrue("Should not be empty", !filter.isEmpty());
        assertTrue("Should have multiple filters", filter.filterCount() > 1);
        
        filter.clear();
        
        assertTrue("Should be empty after clear", filter.isEmpty());
        assertEquals("Should have only 1 filter after clear", 1, filter.filterCount());
        assertFalse("Should not contain items after clear", filter.contains("item0"));
    }
    
    @Test
    public void testScalableBloomFilterCheckAndInsert() {
        ScalableBloomFilter<String> filter = new ScalableBloomFilter<>(
                100, 0.01, BloomFilter.stringSerializer());
        
        assertFalse("First check should return false", filter.checkAndInsert("test"));
        assertTrue("Second check should return true", filter.checkAndInsert("test"));
    }
    
    @Test
    public void testScalableBloomFilterEmpty() {
        ScalableBloomFilter<String> filter = new ScalableBloomFilter<>(
                100, 0.01, BloomFilter.stringSerializer());
        assertTrue("New filter should be empty", filter.isEmpty());
        assertEquals("New filter size should be 0", 0, filter.size());
    }
}