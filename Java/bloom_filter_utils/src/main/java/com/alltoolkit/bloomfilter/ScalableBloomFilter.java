package com.alltoolkit.bloomfilter;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/**
 * Scalable Bloom Filter that grows as needed
 * 
 * This implementation uses multiple Bloom filters that are created on-demand
 * as the current filter fills up. Each new filter has a larger capacity and
 * tighter error rate, maintaining the overall false positive rate.
 * 
 * @param <T> the type of elements to be stored in the filter
 */
public class ScalableBloomFilter<T> {
    
    private final List<BloomFilter<T>> filters;
    private final int initialCapacity;
    private final double errorRate;
    private final double growthFactor;
    private final double tighteningRatio;
    private int itemCount;
    private final BloomFilter.ElementSerializer<T> serializer;
    
    /**
     * Create a new scalable Bloom filter
     * 
     * @param initialCapacity Initial expected number of items
     * @param errorRate Desired overall false positive rate
     * @param serializer Element serializer
     */
    public ScalableBloomFilter(int initialCapacity, double errorRate, 
                               BloomFilter.ElementSerializer<T> serializer) {
        if (initialCapacity <= 0) {
            throw new IllegalArgumentException("Initial capacity must be positive");
        }
        if (errorRate <= 0.0 || errorRate >= 1.0) {
            throw new IllegalArgumentException("Error rate must be between 0 and 1");
        }
        
        this.initialCapacity = initialCapacity;
        this.errorRate = errorRate;
        this.growthFactor = 2.0;
        this.tighteningRatio = 0.5;
        this.serializer = Objects.requireNonNull(serializer, "Serializer cannot be null");
        
        // Create first filter
        this.filters = new ArrayList<>();
        this.filters.add(new BloomFilter<>(initialCapacity, errorRate * 0.5, serializer));
        this.itemCount = 0;
    }
    
    /**
     * Insert an item
     */
    public synchronized void insert(T item) {
        // Check if current filter is getting full
        BloomFilter<T> last = filters.get(filters.size() - 1);
        
        if (last.fillRatio() > 0.5) {
            // Create new filter with larger capacity
            int capacity = (int) (initialCapacity * Math.pow(growthFactor, filters.size()));
            double filterErrorRate = errorRate * Math.pow(tighteningRatio, filters.size() + 1);
            filters.add(new BloomFilter<>(capacity, filterErrorRate, serializer));
        }
        
        filters.get(filters.size() - 1).insert(item);
        itemCount++;
    }
    
    /**
     * Check if item might be present
     */
    public synchronized boolean contains(T item) {
        for (BloomFilter<T> filter : filters) {
            if (filter.contains(item)) {
                return true;
            }
        }
        return false;
    }
    
    /**
     * Check if an item is present, and insert if not
     * @return true if item was already present (or false positive)
     */
    public synchronized boolean checkAndInsert(T item) {
        boolean exists = contains(item);
        if (!exists) {
            insert(item);
        }
        return exists;
    }
    
    /**
     * Get total number of items
     */
    public synchronized int size() {
        return itemCount;
    }
    
    /**
     * Check if empty
     */
    public synchronized boolean isEmpty() {
        return itemCount == 0;
    }
    
    /**
     * Get number of internal filters
     */
    public synchronized int filterCount() {
        return filters.size();
    }
    
    /**
     * Clear all filters
     */
    public synchronized void clear() {
        filters.clear();
        filters.add(new BloomFilter<>(initialCapacity, errorRate * 0.5, serializer));
        itemCount = 0;
    }
    
    /**
     * Estimate overall false positive rate
     */
    public synchronized double estimatedFalsePositiveRate() {
        if (filters.isEmpty()) {
            return 0.0;
        }
        
        // Use the tightest filter's error rate as estimate
        return errorRate * Math.pow(tighteningRatio, filters.size() - 1);
    }
    
    /**
     * Get the total bit count across all filters
     */
    public synchronized int totalBitCount() {
        return filters.stream()
                .mapToInt(BloomFilter::bitCount)
                .sum();
    }
    
    @Override
    public String toString() {
        return String.format("ScalableBloomFilter{filters=%d, items=%d, estFPR=%.6f}",
                filters.size(), itemCount, estimatedFalsePositiveRate());
    }
}