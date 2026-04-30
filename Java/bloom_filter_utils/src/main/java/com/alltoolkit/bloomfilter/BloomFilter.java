package com.alltoolkit.bloomfilter;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Objects;

/**
 * Bloom Filter Implementation
 * 
 * A Bloom filter is a space-efficient probabilistic data structure used to test
 * whether an element is a member of a set. False positives are possible but
 * false negatives are not.
 * 
 * Features:
 * - Zero external dependencies
 * - Configurable false positive rate
 * - Generic type support via byte array conversion
 * - Serialization support
 * - Thread-safe operations available via BloomFilter.concurrent()
 * 
 * @param <T> the type of elements to be stored in the filter
 */
public class BloomFilter<T> {
    
    private final long[] bits;
    private final BloomConfig config;
    private int itemCount;
    private final ElementSerializer<T> serializer;
    
    /**
     * Configuration for a Bloom filter
     */
    public static class BloomConfig {
        private final int size;
        private final int hashCount;
        
        public BloomConfig(int size, int hashCount) {
            if (size <= 0) {
                throw new IllegalArgumentException("Size must be positive");
            }
            if (hashCount <= 0 || hashCount > 32) {
                throw new IllegalArgumentException("Hash count must be between 1 and 32");
            }
            this.size = size;
            this.hashCount = hashCount;
        }
        
        public int getSize() {
            return size;
        }
        
        public int getHashCount() {
            return hashCount;
        }
        
        /**
         * Create optimal config for expected items and desired false positive rate
         * 
         * @param expectedItems Expected number of items to insert
         * @param falsePositiveRate Desired false positive rate (0.0 to 1.0)
         * @return Optimal configuration for the given parameters
         */
        public static BloomConfig optimal(int expectedItems, double falsePositiveRate) {
            if (expectedItems <= 0) {
                throw new IllegalArgumentException("Expected items must be positive");
            }
            if (falsePositiveRate <= 0.0 || falsePositiveRate >= 1.0) {
                throw new IllegalArgumentException("False positive rate must be between 0 and 1");
            }
            
            double ln2 = Math.log(2);
            double ln2Sq = ln2 * ln2;
            
            // Optimal size: m = -n * ln(p) / ln(2)^2
            int size = (int) Math.ceil(-((double) expectedItems * Math.log(falsePositiveRate)) / ln2Sq);
            size = Math.max(64, size);
            
            // Optimal hash count: k = m/n * ln(2)
            int hashCount = (int) Math.ceil((double) size / expectedItems * ln2);
            hashCount = Math.max(1, Math.min(32, hashCount));
            
            return new BloomConfig(size, hashCount);
        }
        
        /**
         * Calculate expected false positive rate for given number of items
         */
        public double expectedFalsePositiveRate(int numItems) {
            if (size == 0 || numItems == 0) {
                return 0.0;
            }
            
            // P(false positive) ≈ (1 - e^(-kn/m))^k
            double ratio = (double) (hashCount * numItems) / size;
            double inner = 1.0 - Math.exp(-ratio);
            return Math.pow(inner, hashCount);
        }
    }
    
    /**
     * Interface for serializing elements to byte arrays
     */
    @FunctionalInterface
    public interface ElementSerializer<T> {
        byte[] serialize(T element);
    }
    
    /**
     * Create a new Bloom filter with the given configuration
     */
    public BloomFilter(BloomConfig config, ElementSerializer<T> serializer) {
        this.config = Objects.requireNonNull(config, "Config cannot be null");
        this.serializer = Objects.requireNonNull(serializer, "Serializer cannot be null");
        int numWords = (config.size + 63) / 64;
        this.bits = new long[numWords];
        this.itemCount = 0;
    }
    
    /**
     * Create a Bloom filter optimized for expected items and false positive rate
     */
    public BloomFilter(int expectedItems, double falsePositiveRate, ElementSerializer<T> serializer) {
        this(BloomConfig.optimal(expectedItems, falsePositiveRate), serializer);
    }
    
    /**
     * Create a Bloom filter with default settings (10000 items, 1% false positive rate)
     */
    public BloomFilter(ElementSerializer<T> serializer) {
        this(10000, 0.01, serializer);
    }
    
    // ========== Built-in serializers ==========
    
    /**
     * Serializer for String elements
     */
    public static ElementSerializer<String> stringSerializer() {
        return s -> s == null ? new byte[0] : s.getBytes(StandardCharsets.UTF_8);
    }
    
    /**
     * Serializer for Integer elements
     */
    public static ElementSerializer<Integer> intSerializer() {
        return i -> {
            byte[] bytes = new byte[4];
            bytes[0] = (byte) (i >> 24);
            bytes[1] = (byte) (i >> 16);
            bytes[2] = (byte) (i >> 8);
            bytes[3] = (byte) i.intValue();
            return bytes;
        };
    }
    
    /**
     * Serializer for Long elements
     */
    public static ElementSerializer<Long> longSerializer() {
        return l -> {
            byte[] bytes = new byte[8];
            long val = l;
            for (int i = 0; i < 8; i++) {
                bytes[i] = (byte) (val >> (56 - i * 8));
            }
            return bytes;
        };
    }
    
    /**
     * Serializer for byte array elements (identity)
     */
    public static ElementSerializer<byte[]> bytesSerializer() {
        return b -> b == null ? new byte[0] : b.clone();
    }
    
    // ========== Core Operations ==========
    
    /**
     * Insert an item into the filter
     */
    public synchronized void insert(T item) {
        byte[] data = serializer.serialize(item);
        long[] hashes = getHashes(data);
        
        for (int i = 0; i < config.hashCount; i++) {
            int bitIndex = getBitIndex(hashes, i);
            setBit(bitIndex);
        }
        itemCount++;
    }
    
    /**
     * Check if an item might be in the filter
     * 
     * Returns true if the item might be present (may have false positives)
     * Returns false if the item is definitely not present (no false negatives)
     */
    public synchronized boolean contains(T item) {
        byte[] data = serializer.serialize(item);
        long[] hashes = getHashes(data);
        
        for (int i = 0; i < config.hashCount; i++) {
            int bitIndex = getBitIndex(hashes, i);
            if (!getBit(bitIndex)) {
                return false;
            }
        }
        return true;
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
     * Clear all items from the filter
     */
    public synchronized void clear() {
        Arrays.fill(bits, 0L);
        itemCount = 0;
    }
    
    // ========== Statistics ==========
    
    /**
     * Get the number of items inserted
     */
    public synchronized int size() {
        return itemCount;
    }
    
    /**
     * Check if the filter is empty
     */
    public synchronized boolean isEmpty() {
        return itemCount == 0;
    }
    
    /**
     * Get the current false positive rate based on number of items
     */
    public synchronized double currentFalsePositiveRate() {
        return config.expectedFalsePositiveRate(itemCount);
    }
    
    /**
     * Get the filter configuration
     */
    public BloomConfig getConfig() {
        return config;
    }
    
    /**
     * Get the number of bits set in the filter
     */
    public synchronized int bitCount() {
        int count = 0;
        for (long word : bits) {
            count += Long.bitCount(word);
        }
        return count;
    }
    
    /**
     * Get fill ratio (proportion of bits set)
     */
    public synchronized double fillRatio() {
        if (config.size == 0) {
            return 0.0;
        }
        return (double) bitCount() / config.size;
    }
    
    // ========== Merge Operations ==========
    
    /**
     * Merge another Bloom filter into this one
     * Both filters must have the same configuration
     */
    public synchronized void merge(BloomFilter<T> other) throws IllegalArgumentException {
        if (this.config.size != other.config.size || 
            this.config.hashCount != other.config.hashCount) {
            throw new IllegalArgumentException("Cannot merge Bloom filters with different configurations");
        }
        
        for (int i = 0; i < bits.length; i++) {
            this.bits[i] |= other.bits[i];
        }
        
        this.itemCount = Math.max(this.itemCount, other.itemCount);
    }
    
    // ========== Serialization ==========
    
    /**
     * Convert filter to bytes for storage
     */
    public synchronized byte[] toBytes() throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        DataOutputStream dos = new DataOutputStream(baos);
        
        // Header
        dos.writeInt(config.size);
        dos.writeInt(config.hashCount);
        dos.writeInt(itemCount);
        
        // Bits
        for (long word : bits) {
            dos.writeLong(word);
        }
        
        dos.flush();
        return baos.toByteArray();
    }
    
    /**
     * Create filter from bytes
     */
    public static <T> BloomFilter<T> fromBytes(byte[] bytes, ElementSerializer<T> serializer) 
            throws IOException {
        if (bytes == null || bytes.length < 12) {
            throw new IllegalArgumentException("Invalid bytes: too short");
        }
        
        ByteArrayInputStream bais = new ByteArrayInputStream(bytes);
        DataInputStream dis = new DataInputStream(bais);
        
        int size = dis.readInt();
        int hashCount = dis.readInt();
        int itemCount = dis.readInt();
        
        BloomConfig config = new BloomConfig(size, hashCount);
        BloomFilter<T> filter = new BloomFilter<>(config, serializer);
        
        int numWords = (size + 63) / 64;
        for (int i = 0; i < numWords; i++) {
            filter.bits[i] = dis.readLong();
        }
        
        filter.itemCount = itemCount;
        return filter;
    }
    
    // ========== Internal Helper Methods ==========
    
    private long[] getHashes(byte[] data) {
        // MurmurHash3-like hashing
        long h1 = murmur3Hash(data, 0);
        long h2 = murmur3Hash(data, 0xDEADBEEF);
        return new long[]{h1, h2};
    }
    
    private int getBitIndex(long[] hashes, int i) {
        // Double hashing: h(i) = h1 + i * h2
        long combined = hashes[0] + (long) i * hashes[1];
        return (int) Math.abs(combined % config.size);
    }
    
    private void setBit(int index) {
        int wordIndex = index / 64;
        int bitOffset = index % 64;
        bits[wordIndex] |= (1L << bitOffset);
    }
    
    private boolean getBit(int index) {
        int wordIndex = index / 64;
        int bitOffset = index % 64;
        return ((bits[wordIndex] >> bitOffset) & 1L) == 1L;
    }
    
    /**
     * Simple MurmurHash3-like hash function
     */
    private long murmur3Hash(byte[] data, int seed) {
        long h = seed;
        int len = data.length;
        
        // Process 8-byte chunks
        int i = 0;
        for (; i + 7 < len; i += 8) {
            long k = ((long) data[i] & 0xFF)
                   | (((long) data[i + 1] & 0xFF) << 8)
                   | (((long) data[i + 2] & 0xFF) << 16)
                   | (((long) data[i + 3] & 0xFF) << 24)
                   | (((long) data[i + 4] & 0xFF) << 32)
                   | (((long) data[i + 5] & 0xFF) << 40)
                   | (((long) data[i + 6] & 0xFF) << 48)
                   | (((long) data[i + 7] & 0xFF) << 56);
            
            k *= 0x87c37b91114253d5L;
            k = Long.rotateLeft(k, 31);
            k *= 0x4cf5ad432745937fL;
            
            h ^= k;
            h = Long.rotateLeft(h, 27);
            h = h * 5 + 0x52dce729;
        }
        
        // Process remaining bytes
        long k = 0;
        int shift = 0;
        for (; i < len; i++) {
            k |= ((long) data[i] & 0xFF) << shift;
            shift += 8;
        }
        
        if (shift > 0) {
            k *= 0x87c37b91114253d5L;
            k = Long.rotateLeft(k, 31);
            k *= 0x4cf5ad432745937fL;
            h ^= k;
        }
        
        // Finalization
        h ^= len;
        h ^= (h >>> 33);
        h *= 0xff51afd7ed558ccdL;
        h ^= (h >>> 33);
        h *= 0xc4ceb9fe1a85ec53L;
        h ^= (h >>> 33);
        
        return h;
    }
    
    @Override
    public String toString() {
        return String.format("BloomFilter{size=%d, hashCount=%d, items=%d, fillRatio=%.4f}",
                config.size, config.hashCount, itemCount, fillRatio());
    }
}