const std = @import("std");
const bloom_filter = @import("bloom_filter");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== Bloom Filter Demo ===\n\n", .{});

    // Basic Bloom Filter
    std.debug.print("--- Basic Bloom Filter ---\n", .{});
    
    var bf = try bloom_filter.BloomFilter.init(allocator, .{
        .expected_items = 1000,
        .false_positive_rate = 0.01,
    });
    defer bf.deinit();

    std.debug.print("Filter size: {} bits, {} hash functions\n", .{
        bf.bitCount(),
        bf.hashFunctionCount(),
    });

    // Add some fruits
    const fruits = [_][]const u8{ "apple", "banana", "cherry", "date", "elderberry" };
    for (fruits) |fruit| {
        bf.add(fruit);
        std.debug.print("Added: {s}\n", .{fruit});
    }

    std.debug.print("\nItems inserted: {}\n", .{bf.itemCount()});
    std.debug.print("Bits set: {}\n", .{bf.bitsSet()});
    std.debug.print("Estimated FP rate: {:.4}\n", .{bf.estimateFalsePositiveRate()});

    // Check membership
    std.debug.print("\nMembership tests:\n", .{});
    const test_items = [_][]const u8{ "apple", "banana", "fig", "grape", "kiwi" };
    for (test_items) |item| {
        const result = bf.mightContain(item);
        if (result) {
            std.debug.print("  {s}: possibly in set\n", .{item});
        } else {
            std.debug.print("  {s}: definitely NOT in set\n", .{item});
        }
    }

    // Integer operations
    std.debug.print("\n--- Integer Operations ---\n", .{});
    bf.addU64(42);
    bf.addU64(100);
    bf.addU64(999);

    const test_numbers = [_]u64{ 42, 100, 999, 123, 456 };
    for (test_numbers) |num| {
        const result = bf.mightContainU64(num);
        std.debug.print("  {}: {}\n", .{ num, result });
    }

    // Counting Bloom Filter
    std.debug.print("\n--- Counting Bloom Filter (supports removal) ---\n", .{});
    
    var cbf = try bloom_filter.CountingBloomFilter.init(allocator, .{
        .expected_items = 100,
        .false_positive_rate = 0.01,
    });
    defer cbf.deinit();

    cbf.add("red");
    cbf.add("green");
    cbf.add("blue");
    std.debug.print("Added colors: red, green, blue\n", .{});

    std.debug.print("Before removal:\n", .{});
    std.debug.print("  red: {}\n", .{cbf.mightContain("red")});
    std.debug.print("  green: {}\n", .{cbf.mightContain("green")});
    std.debug.print("  blue: {}\n", .{cbf.mightContain("blue")});

    // Remove an item
    if (cbf.remove("green")) {
        std.debug.print("\nRemoved 'green'\n", .{});
    }

    std.debug.print("After removal:\n", .{});
    std.debug.print("  red: {}\n", .{cbf.mightContain("red")});
    std.debug.print("  green: {}\n", .{cbf.mightContain("green")});
    std.debug.print("  blue: {}\n", .{cbf.mightContain("blue")});

    // Scalable Bloom Filter
    std.debug.print("\n--- Scalable Bloom Filter (auto-expands) ---\n", .{});
    
    var sbf = try bloom_filter.ScalableBloomFilter.init(allocator, 0.01);
    defer sbf.deinit();

    std.debug.print("Adding 500 items...\n", .{});
    for (0..500) |i| {
        var buf: [20]u8 = undefined;
        const str = std.fmt.bufPrint(&buf, "user_{}", .{i}) catch unreachable;
        sbf.add(str);
    }

    std.debug.print("Total filters: {}\n", .{sbf.filters.items.len});
    std.debug.print("Total items: {}\n", .{sbf.itemCount()});

    // Test some items
    std.debug.print("\nTesting items:\n", .{});
    std.debug.print("  user_0: {}\n", .{sbf.mightContain("user_0")});
    std.debug.print("  user_100: {}\n", .{sbf.mightContain("user_100")});
    std.debug.print("  user_499: {}\n", .{sbf.mightContain("user_499")});
    std.debug.print("  nonexistent: {}\n", .{sbf.mightContain("nonexistent")});

    // Union operation
    std.debug.print("\n--- Union Operation ---\n", .{});
    
    var bf1 = try bloom_filter.BloomFilter.initWithParams(allocator, 1000, 5);
    defer bf1.deinit();
    
    var bf2 = try bloom_filter.BloomFilter.initWithParams(allocator, 1000, 5);
    defer bf2.deinit();

    bf1.add("cat");
    bf1.add("dog");
    bf2.add("bird");
    bf2.add("fish");

    try bf1.unionWith(&bf2);

    std.debug.print("After union:\n", .{});
    std.debug.print("  cat: {}\n", .{bf1.mightContain("cat")});
    std.debug.print("  dog: {}\n", .{bf1.mightContain("dog")});
    std.debug.print("  bird: {}\n", .{bf1.mightContain("bird")});
    std.debug.print("  fish: {}\n", .{bf1.mightContain("fish")});

    // Serialization
    std.debug.print("\n--- Serialization ---\n", .{});
    
    var bf_orig = try bloom_filter.BloomFilter.init(allocator, .{
        .expected_items = 100,
        .false_positive_rate = 0.01,
    });
    defer bf_orig.deinit();

    bf_orig.add("saved_item_1");
    bf_orig.add("saved_item_2");
    bf_orig.add("saved_item_3");

    const serialized = try bf_orig.serialize(allocator);
    defer allocator.free(serialized);

    std.debug.print("Serialized size: {} bytes\n", .{serialized.len});

    var bf_restored = try bloom_filter.BloomFilter.deserialize(allocator, serialized);
    defer bf_restored.deinit();

    std.debug.print("Restored filter checks:\n", .{});
    std.debug.print("  saved_item_1: {}\n", .{bf_restored.mightContain("saved_item_1")});
    std.debug.print("  saved_item_2: {}\n", .{bf_restored.mightContain("saved_item_2")});
    std.debug.print("  saved_item_3: {}\n", .{bf_restored.mightContain("saved_item_3")});
    std.debug.print("  unknown_item: {}\n", .{bf_restored.mightContain("unknown_item")});

    std.debug.print("\n=== Demo Complete ===\n", .{});
}