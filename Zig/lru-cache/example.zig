const std = @import("std");
const LruCache = @import("lru_cache.zig").LruCache;

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    
    // Example 1: Basic usage
    std.debug.print("\n=== LRU Cache Examples ===\n\n", .{});
    std.debug.print("Example 1: Basic Cache Operations\n", .{});
    std.debug.print("---------------------------------\n", .{});
    
    var cache = try LruCache(u32, u32).init(allocator, 3);
    defer cache.deinit();
    
    try cache.put(1, 100);
    try cache.put(2, 200);
    try cache.put(3, 300);
    
    std.debug.print("Cache size: {} (capacity: {})\n", .{ cache.getSize(), cache.getCapacity() });
    std.debug.print("Key 1: {?}\n", .{ cache.get(1) });
    std.debug.print("Key 2: {?}\n", .{ cache.get(2) });
    std.debug.print("Key 4: {?}\n", .{ cache.get(4) }); // Not found
    
    // Example 2: Eviction
    std.debug.print("\nExample 2: LRU Eviction\n", .{});
    std.debug.print("------------------------\n", .{});
    
    std.debug.print("Adding key 4 = 400 (should evict least recently used)...\n", .{});
    try cache.put(4, 400);
    
    std.debug.print("After eviction:\n", .{});
    std.debug.print("  Key 1: {?} (evicted)\n", .{ cache.get(1) });
    std.debug.print("  Key 2: {?}\n", .{ cache.get(2) });
    std.debug.print("  Key 3: {?}\n", .{ cache.get(3) });
    std.debug.print("  Key 4: {?}\n", .{ cache.get(4) });
    
    // Example 3: Access order affects eviction
    std.debug.print("\nExample 3: Access Order Affects Eviction\n", .{});
    std.debug.print("------------------------------------------\n", .{});
    
    var cache2 = try LruCache(u32, u32).init(allocator, 3);
    defer cache2.deinit();
    
    try cache2.put(1, 100);
    try cache2.put(2, 200);
    try cache2.put(3, 300);
    
    std.debug.print("Initial: [1=100, 2=200, 3=300]\n", .{});
    
    _ = cache2.get(1); // Access 1, making it most recently used
    std.debug.print("Access key 1 (now most recently used)\n", .{});
    
    try cache2.put(4, 400); // Should evict 2 (least recently used now)
    std.debug.print("Add key 4\n", .{});
    std.debug.print("  Key 1: {?} (kept - recently accessed)\n", .{ cache2.get(1) });
    std.debug.print("  Key 2: {?} (evicted)\n", .{ cache2.get(2) });
    std.debug.print("  Key 3: {?}\n", .{ cache2.get(3) });
    std.debug.print("  Key 4: {?}\n", .{ cache2.get(4) });
    
    // Example 4: Update existing key
    std.debug.print("\nExample 4: Updating Existing Values\n", .{});
    std.debug.print("-------------------------------------\n", .{});
    
    var cache3 = try LruCache(u32, u32).init(allocator, 2);
    defer cache3.deinit();
    
    try cache3.put(1, 100);
    std.debug.print("Put key 1 = 100\n", .{});
    std.debug.print("  Get key 1: {?}\n", .{ cache3.get(1) });
    
    try cache3.put(1, 200);
    std.debug.print("Put key 1 = 200\n", .{});
    std.debug.print("  Get key 1: {?}\n", .{ cache3.get(1) });
    std.debug.print("  Size: {} (no duplicate)\n", .{ cache3.getSize() });
    
    // Example 5: Remove and contains
    std.debug.print("\nExample 5: Remove and Contains\n", .{});
    std.debug.print("-------------------------------\n", .{});
    
    var cache4 = try LruCache(u32, u32).init(allocator, 3);
    defer cache4.deinit();
    
    try cache4.put(10, 1000);
    try cache4.put(20, 2000);
    
    std.debug.print("Contains 10: {}\n", .{ cache4.contains(10) });
    std.debug.print("Contains 30: {}\n", .{ cache4.contains(30) });
    
    const removed = cache4.remove(10);
    std.debug.print("Removed 10: {}\n", .{ removed });
    std.debug.print("Contains 10 after removal: {}\n", .{ cache4.contains(10) });
    
    // Example 6: Iterator
    std.debug.print("\nExample 6: Iterating Over Cache\n", .{});
    std.debug.print("---------------------------------\n", .{});
    
    var cache5 = try LruCache(u32, u32).init(allocator, 4);
    defer cache5.deinit();
    
    try cache5.put(1, 100);
    try cache5.put(2, 200);
    try cache5.put(3, 300);
    
    std.debug.print("Cache contents (most to least recently used):\n", .{});
    var iter = cache5.iterator();
    while (iter.next()) |entry| {
        std.debug.print("  {} = {}\n", .{ entry.key, entry.value });
    }
    
    // Example 7: Clear cache
    std.debug.print("\nExample 7: Clear Cache\n", .{});
    std.debug.print("-----------------------\n", .{});
    
    try cache5.put(4, 400);
    std.debug.print("Before clear: size = {}\n", .{ cache5.getSize() });
    
    cache5.clear();
    std.debug.print("After clear: size = {}\n", .{ cache5.getSize() });
    
    std.debug.print("\n=== Examples Complete ===\n", .{});
}