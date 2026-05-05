const std = @import("std");
const Allocator = std.mem.Allocator;

/// LRU (Least Recently Used) Cache implementation
/// A fixed-size cache that evicts the least recently used entry when full
pub fn LruCache(comptime K: type, comptime V: type) type {
    return struct {
        const Self = @This();
        
        const Node = struct {
            key: K,
            value: V,
            prev: ?*Node,
            next: ?*Node,
        };
        
        allocator: Allocator,
        capacity: usize,
        size: usize,
        head: ?*Node,
        tail: ?*Node,
        map: std.AutoHashMap(K, *Node),
        
        /// Initialize a new LRU cache with the given capacity
        pub fn init(allocator: Allocator, capacity: usize) !Self {
            return Self{
                .allocator = allocator,
                .capacity = capacity,
                .size = 0,
                .head = null,
                .tail = null,
                .map = std.AutoHashMap(K, *Node).init(allocator),
            };
        }
        
        /// Free all allocated memory
        pub fn deinit(self: *Self) void {
            // Free all nodes
            var current = self.head;
            while (current) |node| {
                const next = node.next;
                self.allocator.destroy(node);
                current = next;
            }
            self.map.deinit();
            self.* = undefined;
        }
        
        /// Get a value from the cache
        /// Returns null if not found, moves the item to the front (most recently used)
        pub fn get(self: *Self, key: K) ?V {
            if (self.map.get(key)) |node| {
                // Move to front
                self.moveToFront(node);
                return node.value;
            }
            return null;
        }
        
        /// Put a value into the cache
        /// If the key exists, updates the value and moves to front
        /// If the cache is full, evicts the least recently used item
        pub fn put(self: *Self, key: K, value: V) !void {
            if (self.map.get(key)) |node| {
                // Update existing node
                node.value = value;
                self.moveToFront(node);
                return;
            }
            
            // Create new node
            const node = try self.allocator.create(Node);
            node.* = Node{
                .key = key,
                .value = value,
                .prev = null,
                .next = null,
            };
            
            // Check if we need to evict
            if (self.size >= self.capacity) {
                self.evict();
            }
            
            // Add to front
            self.addToFront(node);
            try self.map.put(key, node);
            self.size += 1;
        }
        
        /// Check if a key exists in the cache
        pub fn contains(self: *Self, key: K) bool {
            return self.map.contains(key);
        }
        
        /// Remove a key from the cache
        pub fn remove(self: *Self, key: K) bool {
            if (self.map.get(key)) |node| {
                self.removeNode(node);
                _ = self.map.remove(key);
                self.allocator.destroy(node);
                self.size -= 1;
                return true;
            }
            return false;
        }
        
        /// Clear all items from the cache
        pub fn clear(self: *Self) void {
            var current = self.head;
            while (current) |node| {
                const next = node.next;
                self.allocator.destroy(node);
                current = next;
            }
            self.map.clearRetainingCapacity();
            self.head = null;
            self.tail = null;
            self.size = 0;
        }
        
        /// Get current size of the cache
        pub fn getSize(self: *Self) usize {
            return self.size;
        }
        
        /// Get the capacity of the cache
        pub fn getCapacity(self: *Self) usize {
            return self.capacity;
        }
        
        /// Get all keys in order from most to least recently used
        pub fn keys(self: *Self, allocator: Allocator) ![]K {
            var result = std.ArrayList(K).init(allocator);
            var current = self.head;
            while (current) |node| {
                try result.append(node.key);
                current = node.next;
            }
            return result.toOwnedSlice();
        }
        
        // Private helper methods
        
        fn moveToFront(self: *Self, node: *Node) void {
            if (self.head == node) return;
            
            // Remove from current position
            self.removeNode(node);
            
            // Add to front
            self.addToFront(node);
        }
        
        fn addToFront(self: *Self, node: *Node) void {
            node.prev = null;
            node.next = self.head;
            
            if (self.head) |head| {
                head.prev = node;
            }
            self.head = node;
            
            if (self.tail == null) {
                self.tail = node;
            }
        }
        
        fn removeNode(self: *Self, node: *Node) void {
            if (node.prev) |prev| {
                prev.next = node.next;
            } else {
                self.head = node.next;
            }
            
            if (node.next) |next| {
                next.prev = node.prev;
            } else {
                self.tail = node.prev;
            }
        }
        
        fn evict(self: *Self) void {
            if (self.tail) |tail| {
                _ = self.map.remove(tail.key);
                self.removeNode(tail);
                self.allocator.destroy(tail);
                self.size -= 1;
            }
        }
        
        /// Iterator over cache entries from most to least recently used
        pub const Iterator = struct {
            current: ?*Node,
            
            pub fn next(self: *Iterator) ?struct { key: K, value: V } {
                if (self.current) |node| {
                    self.current = node.next;
                    return .{ .key = node.key, .value = node.value };
                }
                return null;
            }
        };
        
        /// Get an iterator over cache entries
        pub fn iterator(self: *Self) Iterator {
            return .{ .current = self.head };
        }
    };
}

// Tests
test "LruCache - basic put and get" {
    const allocator = std.testing.allocator;
    var cache = try LruCache(u32, u32).init(allocator, 3);
    defer cache.deinit();
    
    try cache.put(1, 100);
    try cache.put(2, 200);
    try cache.put(3, 300);
    
    try std.testing.expectEqual(@as(?u32, 100), cache.get(1));
    try std.testing.expectEqual(@as(?u32, 200), cache.get(2));
    try std.testing.expectEqual(@as(?u32, 300), cache.get(3));
    try std.testing.expectEqual(@as(usize, 3), cache.getSize());
}

test "LruCache - eviction" {
    const allocator = std.testing.allocator;
    var cache = try LruCache(u32, u32).init(allocator, 2);
    defer cache.deinit();
    
    try cache.put(1, 100);
    try cache.put(2, 200);
    try cache.put(3, 300); // Should evict 1
    
    try std.testing.expectEqual(@as(?u32, null), cache.get(1));
    try std.testing.expectEqual(@as(?u32, 200), cache.get(2));
    try std.testing.expectEqual(@as(?u32, 300), cache.get(3));
}

test "LruCache - LRU order" {
    const allocator = std.testing.allocator;
    var cache = try LruCache(u32, u32).init(allocator, 3);
    defer cache.deinit();
    
    try cache.put(1, 100);
    try cache.put(2, 200);
    try cache.put(3, 300);
    
    _ = cache.get(1); // Access 1, now it's most recently used
    
    try cache.put(4, 400); // Should evict 2 (least recently used)
    
    try std.testing.expectEqual(@as(?u32, 100), cache.get(1));
    try std.testing.expectEqual(@as(?u32, null), cache.get(2));
    try std.testing.expectEqual(@as(?u32, 300), cache.get(3));
    try std.testing.expectEqual(@as(?u32, 400), cache.get(4));
}

test "LruCache - update existing" {
    const allocator = std.testing.allocator;
    var cache = try LruCache(u32, u32).init(allocator, 2);
    defer cache.deinit();
    
    try cache.put(1, 100);
    try cache.put(1, 200); // Update
    
    try std.testing.expectEqual(@as(?u32, 200), cache.get(1));
    try std.testing.expectEqual(@as(usize, 1), cache.getSize());
}

test "LruCache - remove" {
    const allocator = std.testing.allocator;
    var cache = try LruCache(u32, u32).init(allocator, 3);
    defer cache.deinit();
    
    try cache.put(1, 100);
    try cache.put(2, 200);
    
    try std.testing.expectEqual(true, cache.remove(1));
    try std.testing.expectEqual(@as(?u32, null), cache.get(1));
    try std.testing.expectEqual(@as(usize, 1), cache.getSize());
    try std.testing.expectEqual(false, cache.remove(999)); // Non-existent
}

test "LruCache - clear" {
    const allocator = std.testing.allocator;
    var cache = try LruCache(u32, u32).init(allocator, 3);
    defer cache.deinit();
    
    try cache.put(1, 100);
    try cache.put(2, 200);
    try cache.put(3, 300);
    
    cache.clear();
    
    try std.testing.expectEqual(@as(usize, 0), cache.getSize());
    try std.testing.expectEqual(@as(?u32, null), cache.get(1));
}

test "LruCache - contains" {
    const allocator = std.testing.allocator;
    var cache = try LruCache(u32, u32).init(allocator, 2);
    defer cache.deinit();
    
    try cache.put(1, 100);
    
    try std.testing.expectEqual(true, cache.contains(1));
    try std.testing.expectEqual(false, cache.contains(2));
}

test "LruCache - iterator" {
    const allocator = std.testing.allocator;
    var cache = try LruCache(u32, u32).init(allocator, 3);
    defer cache.deinit();
    
    try cache.put(1, 100);
    try cache.put(2, 200);
    try cache.put(3, 300);
    
    var iter = cache.iterator();
    var count: usize = 0;
    while (iter.next()) |_| {
        count += 1;
    }
    try std.testing.expectEqual(@as(usize, 3), count);
}