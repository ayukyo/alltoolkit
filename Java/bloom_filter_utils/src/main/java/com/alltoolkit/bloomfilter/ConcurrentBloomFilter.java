package com.alltoolkit.bloomfilter;

import java.io.IOException;
import java.util.Objects;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

/**
 * Thread-safe wrapper for BloomFilter
 * 
 * Provides concurrent access to a Bloom filter using read-write locks.
 * Multiple threads can read simultaneously, while writes are exclusive.
 * 
 * @param <T> the type of elements to be stored in the filter
 */
public class ConcurrentBloomFilter<T> {
    
    private final BloomFilter<T> delegate;
    private final ReadWriteLock lock = new ReentrantReadWriteLock();
    
    /**
     * Create a concurrent wrapper around a Bloom filter
     */
    public ConcurrentBloomFilter(BloomFilter<T> delegate) {
        this.delegate = Objects.requireNonNull(delegate, "Delegate cannot be null");
    }
    
    /**
     * Create a new concurrent Bloom filter with the given configuration
     */
    public ConcurrentBloomFilter(BloomFilter.BloomConfig config, 
                                BloomFilter.ElementSerializer<T> serializer) {
        this(new BloomFilter<>(config, serializer));
    }
    
    /**
     * Create a concurrent Bloom filter optimized for expected items and false positive rate
     */
    public ConcurrentBloomFilter(int expectedItems, double falsePositiveRate, 
                                 BloomFilter.ElementSerializer<T> serializer) {
        this(new BloomFilter<>(expectedItems, falsePositiveRate, serializer));
    }
    
    /**
     * Create a concurrent Bloom filter with default settings
     */
    public ConcurrentBloomFilter(BloomFilter.ElementSerializer<T> serializer) {
        this(new BloomFilter<>(serializer));
    }
    
    // ========== Core Operations ==========
    
    /**
     * Insert an item into the filter
     */
    public void insert(T item) {
        lock.writeLock().lock();
        try {
            delegate.insert(item);
        } finally {
            lock.writeLock().unlock();
        }
    }
    
    /**
     * Check if an item might be in the filter
     */
    public boolean contains(T item) {
        lock.readLock().lock();
        try {
            return delegate.contains(item);
        } finally {
            lock.readLock().unlock();
        }
    }
    
    /**
     * Check if an item is present, and insert if not
     */
    public boolean checkAndInsert(T item) {
        lock.writeLock().lock();
        try {
            return delegate.checkAndInsert(item);
        } finally {
            lock.writeLock().unlock();
        }
    }
    
    /**
     * Clear all items from the filter
     */
    public void clear() {
        lock.writeLock().lock();
        try {
            delegate.clear();
        } finally {
            lock.writeLock().unlock();
        }
    }
    
    // ========== Statistics ==========
    
    /**
     * Get the number of items inserted
     */
    public int size() {
        lock.readLock().lock();
        try {
            return delegate.size();
        } finally {
            lock.readLock().unlock();
        }
    }
    
    /**
     * Check if the filter is empty
     */
    public boolean isEmpty() {
        lock.readLock().lock();
        try {
            return delegate.isEmpty();
        } finally {
            lock.readLock().unlock();
        }
    }
    
    /**
     * Get the current false positive rate
     */
    public double currentFalsePositiveRate() {
        lock.readLock().lock();
        try {
            return delegate.currentFalsePositiveRate();
        } finally {
            lock.readLock().unlock();
        }
    }
    
    /**
     * Get the filter configuration
     */
    public BloomFilter.BloomConfig getConfig() {
        return delegate.getConfig();
    }
    
    /**
     * Get the number of bits set in the filter
     */
    public int bitCount() {
        lock.readLock().lock();
        try {
            return delegate.bitCount();
        } finally {
            lock.readLock().unlock();
        }
    }
    
    /**
     * Get fill ratio
     */
    public double fillRatio() {
        lock.readLock().lock();
        try {
            return delegate.fillRatio();
        } finally {
            lock.readLock().unlock();
        }
    }
    
    // ========== Serialization ==========
    
    /**
     * Convert filter to bytes for storage
     */
    public byte[] toBytes() throws IOException {
        lock.readLock().lock();
        try {
            return delegate.toBytes();
        } finally {
            lock.readLock().unlock();
        }
    }
    
    /**
     * Create concurrent filter from bytes
     */
    public static <T> ConcurrentBloomFilter<T> fromBytes(byte[] bytes, 
                                                         BloomFilter.ElementSerializer<T> serializer) 
            throws IOException {
        BloomFilter<T> filter = BloomFilter.fromBytes(bytes, serializer);
        return new ConcurrentBloomFilter<>(filter);
    }
    
    @Override
    public String toString() {
        lock.readLock().lock();
        try {
            return "Concurrent" + delegate.toString();
        } finally {
            lock.readLock().unlock();
        }
    }
}