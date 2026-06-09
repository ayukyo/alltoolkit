package com.alltoolkit;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.Arrays;

/**
 * Count-Min Sketch - Probabilistic data structure for frequency estimation.
 * Uses sublinear space for counting item frequencies with controlled error bounds.
 */
public class CountMinSketch<T> {
    private final long[][] table;
    private final int depth;
    private final int width;
    private final long seed;
    private long totalCount;

    public CountMinSketch(int depth, int width, long seed) {
        this.depth = Math.max(1, depth);
        this.width = Math.max(2, width);
        this.seed = seed;
        this.table = new long[this.depth][this.width];
        this.totalCount = 0;
    }

    public CountMinSketch(int depth, int width) {
        this(depth, width, 0xDEADBEEFL);
    }

    /**
     * Create with optimal configuration for given epsilon and delta.
     */
    public static CountMinConfig optimal(double epsilon, double delta) {
        int width = (int) Math.ceil(Math.E / epsilon);
        int depth = (int) Math.ceil(-Math.log(delta));
        return new CountMinConfig(
            Math.max(1, depth),
            Math.max(2, width),
            0xDEADBEEFL
        );
    }

    public static <T> CountMinSketch<T> withRate(double epsilon, double delta) {
        CountMinConfig config = optimal(epsilon, delta);
        return new CountMinSketch<>(config.depth, config.width, config.seed);
    }

    /**
     * Update count for item by delta.
     */
    public void update(T item, long delta) {
        long[] hashes = getHashes(item);
        for (int i = 0; i < depth; i++) {
            int idx = (int) hashes[i];
            table[i][idx] += delta;
        }
        totalCount += delta;
    }

    /**
     * Increment count by 1.
     */
    public void increment(T item) {
        update(item, 1);
    }

    /**
     * Estimate count for item (returns upper bound).
     */
    public long estimate(T item) {
        long[] hashes = getHashes(item);
        long min = table[0][(int) hashes[0]];
        for (int i = 1; i < depth; i++) {
            int idx = (int) hashes[i];
            long val = table[i][idx];
            if (val < min) min = val;
        }
        return min;
    }

    public long totalCount() {
        return totalCount;
    }

    public int[] dimensions() {
        return new int[]{depth, width};
    }

    public void merge(CountMinSketch<T> other) throws DimensionMismatchException {
        if (depth != other.depth || width != other.width) {
            throw new DimensionMismatchException(
                "Cannot merge: depth=" + depth + " vs " + other.depth +
                ", width=" + width + " vs " + other.width
            );
        }
        for (int i = 0; i < depth; i++) {
            for (int j = 0; j < width; j++) {
                table[i][j] += other.table[i][j];
            }
        }
        totalCount += other.totalCount;
    }

    public byte[] toBytes() {
        int size = 32 + depth * width * 8;
        ByteBuffer buf = ByteBuffer.allocate(size).order(ByteOrder.LITTLE_ENDIAN);
        buf.putLong(depth);
        buf.putLong(width);
        buf.putLong(seed);
        buf.putLong(totalCount);
        for (int i = 0; i < depth; i++) {
            for (int j = 0; j < width; j++) {
                buf.putLong(table[i][j]);
            }
        }
        return buf.array();
    }

    public static <T> CountMinSketch<T> fromBytes(byte[] bytes) throws InvalidByteException {
        if (bytes.length < 32) throw new InvalidByteException("Too short: " + bytes.length);
        
        ByteBuffer buf = ByteBuffer.wrap(bytes).order(ByteOrder.LITTLE_ENDIAN);
        int d = (int) buf.getLong();
        int w = (int) buf.getLong();
        long s = buf.getLong();
        long tc = buf.getLong();
        
        int expectedLen = 32 + d * w * 8;
        if (bytes.length < expectedLen) throw new InvalidByteException("Invalid length");
        
        CountMinSketch<T> sketch = new CountMinSketch<>(d, w, s);
        sketch.totalCount = tc;
        for (int i = 0; i < d; i++) {
            for (int j = 0; j < w; j++) {
                sketch.table[i][j] = buf.getLong();
            }
        }
        return sketch;
    }

    public void clear() {
        for (int i = 0; i < depth; i++) {
            Arrays.fill(table[i], 0);
        }
        totalCount = 0;
    }

    private long[] getHashes(T item) {
        String str = String.valueOf(item);
        
        long h1 = 0xcbf29ce484222325L;
        for (int i = 0; i < str.length(); i++) {
            h1 = (h1 * 0x100000001b3L) ^ str.charAt(i);
        }
        h1 = (h1 ^ seed) * 0x100000001b3L;
        
        long h2 = seed;
        for (int i = 0; i < str.length(); i++) {
            h2 = (h2 * 0x100000001b3L) ^ str.charAt(i);
        }
        
        long[] hashes = new long[depth];
        for (int i = 0; i < depth; i++) {
            hashes[i] = Math.abs((h1 + i * h2) % width);
        }
        return hashes;
    }

    public static class CountMinConfig {
        public final int depth;
        public final int width;
        public final long seed;

        public CountMinConfig(int depth, int width, long seed) {
            this.depth = depth;
            this.width = width;
            this.seed = seed;
        }
    }

    public static class DimensionMismatchException extends Exception {
        public DimensionMismatchException(String msg) { super(msg); }
    }

    public static class InvalidByteException extends Exception {
        public InvalidByteException(String msg) { super(msg); }
    }

    // Test suite
    public static void runTests() {
        System.out.println("Running Count-Min Sketch tests...");

        // Test 1: Basic increment
        CountMinSketch<String> sketch1 = new CountMinSketch<>(5, 100);
        sketch1.increment("hello");
        sketch1.increment("hello");
        sketch1.increment("world");
        assert sketch1.estimate("hello") >= 2 : "Test 1 failed: hello";
        assert sketch1.estimate("world") >= 1 : "Test 1 failed: world";
        assert sketch1.estimate("missing") == 0 : "Test 1 failed: missing";
        System.out.println("✓ Test 1: Basic increment");

        // Test 2: Update with delta
        CountMinSketch<String> sketch2 = new CountMinSketch<>(5, 100);
        sketch2.update("item", 5);
        assert sketch2.estimate("item") >= 5 : "Test 2 failed";
        System.out.println("✓ Test 2: Update with delta");

        // Test 3: Total count
        CountMinSketch<String> sketch3 = new CountMinSketch<>(5, 100);
        sketch3.increment("a");
        sketch3.update("b", 3);
        sketch3.increment("c");
        assert sketch3.totalCount() == 5 : "Test 3 failed: " + sketch3.totalCount();
        System.out.println("✓ Test 3: Total count");

        // Test 4: Merge
        CountMinSketch<String> sketch4a = new CountMinSketch<>(5, 100);
        CountMinSketch<String> sketch4b = new CountMinSketch<>(5, 100);
        sketch4a.increment("hello");
        sketch4b.increment("world");
        sketch4b.increment("world");
        try {
            sketch4a.merge(sketch4b);
        } catch (DimensionMismatchException e) {
            throw new AssertionError("Merge failed: " + e.getMessage());
        }
        assert sketch4a.estimate("hello") >= 1 : "Test 4 failed: hello";
        assert sketch4a.estimate("world") >= 2 : "Test 4 failed: world";
        System.out.println("✓ Test 4: Merge");

        // Test 5: Clear
        CountMinSketch<String> sketch5 = new CountMinSketch<>(5, 100);
        sketch5.increment("test");
        sketch5.clear();
        assert sketch5.estimate("test") == 0 : "Test 5 failed";
        System.out.println("✓ Test 5: Clear");

        // Test 6: Optimal config
        CountMinConfig config = optimal(0.01, 0.01);
        assert config.depth >= 1 && config.width >= 2 : "Test 6 failed";
        System.out.println("✓ Test 6: Optimal config");

        // Test 7: Serialization
        CountMinSketch<String> sketch7 = withRate("hello");
        sketch7.increment("apple");
        sketch7.increment("banana");
        sketch7.increment("apple");
        byte[] bytes = sketch7.toBytes();
        assert bytes.length > 0 : "Test 7 failed: serialization";
        System.out.println("✓ Test 7: Serialization");

        // Test 8: Dimensions
        CountMinSketch<String> sketch8 = new CountMinSketch<>(7, 200);
        int[] dims = sketch8.dimensions();
        assert dims[0] == 7 && dims[1] == 200 : "Test 8 failed";
        System.out.println("✓ Test 8: Dimensions");

        System.out.println("\n✅ All tests passed!");
    }

    public static <T> CountMinSketch<T> withRate(T item) {
        return withRate(0.01, 0.01);
    }

    public static void main(String[] args) {
        runTests();
    }
}