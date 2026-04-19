const std = @import("std");
const Allocator = std.mem.Allocator;
const Order = std.math.Order;

/// Priority Queue implementation using a binary heap
/// Supports both min-heap and max-heap configurations
pub fn PriorityQueue(comptime T: type) type {
    return struct {
        const Self = @This();

        items: []T,
        len: usize,
        capacity: usize,
        allocator: Allocator,
        compare: *const fn (a: T, b: T) Order,

        /// Initialize a new priority queue
        pub fn init(allocator: Allocator, compare: *const fn (a: T, b: T) Order) Self {
            return .{
                .items = &[_]T{},
                .len = 0,
                .capacity = 0,
                .allocator = allocator,
                .compare = compare,
            };
        }

        /// Initialize with pre-allocated capacity
        pub fn initCapacity(allocator: Allocator, capacity: usize, compare: *const fn (a: T, b: T) Order) Allocator.Error!Self {
            const items = try allocator.alloc(T, capacity);
            return .{
                .items = items,
                .len = 0,
                .capacity = capacity,
                .allocator = allocator,
                .compare = compare,
            };
        }

        /// Free all allocated memory
        pub fn deinit(self: *Self) void {
            if (self.capacity > 0) {
                self.allocator.free(self.items);
            }
            self.* = undefined;
        }

        /// Check if the queue is empty
        pub fn isEmpty(self: Self) bool {
            return self.len == 0;
        }

        /// Get the number of elements
        pub fn count(self: Self) usize {
            return self.len;
        }

        /// Peek at the top element without removing it
        pub fn peek(self: Self) ?T {
            if (self.isEmpty()) return null;
            return self.items[0];
        }

        /// Insert a new element
        pub fn insert(self: *Self, item: T) Allocator.Error!void {
            try self.ensureCapacity(self.len + 1);
            self.items[self.len] = item;
            self.len += 1;
            self.siftUp(self.len - 1);
        }

        /// Remove and return the top element
        pub fn remove(self: *Self) ?T {
            if (self.isEmpty()) return null;
            
            const top = self.items[0];
            self.len -= 1;
            
            if (self.len > 0) {
                self.items[0] = self.items[self.len];
                self.siftDown(0);
            }
            
            return top;
        }

        /// Ensure capacity is at least new_capacity
        pub fn ensureCapacity(self: *Self, new_capacity: usize) Allocator.Error!void {
            if (new_capacity <= self.capacity) return;
            
            const better_capacity = @max(self.capacity * 2, new_capacity);
            const new_items = try self.allocator.realloc(self.items, better_capacity);
            self.items = new_items;
            self.capacity = better_capacity;
        }

        /// Clear all elements (does not free memory)
        pub fn clear(self: *Self) void {
            self.len = 0;
        }

        /// Convert to a sorted slice (caller owns the memory)
        pub fn toSortedSlice(self: *Self, allocator: Allocator) Allocator.Error![]T {
            const result = try allocator.alloc(T, self.len);
            errdefer allocator.free(result);
            
            // Copy elements
            @memcpy(result[0..self.len], self.items[0..self.len]);
            
            // Sort using heap sort
            const Context = struct {
                items: []T,
                compare: *const fn (a: T, b: T) Order,
                
                fn lessThan(ctx: @This(), a: usize, b: usize) bool {
                    return ctx.compare(ctx.items[a], ctx.items[b]) == .lt;
                }
                
                fn swap(ctx: @This(), a: usize, b: usize) void {
                    const tmp = ctx.items[a];
                    ctx.items[a] = ctx.items[b];
                    ctx.items[b] = tmp;
                }
            };
            
            std.sort.heap(result, Context{
                .items = result,
                .compare = self.compare,
            }, Context.lessThan, Context.swap);
            
            return result;
        }

        // Internal: sift up from index
        fn siftUp(self: *Self, index: usize) void {
            var i = index;
            while (i > 0) {
                const parent = (i - 1) / 2;
                if (self.compare(self.items[i], self.items[parent]) == .lt) {
                    self.swap(i, parent);
                    i = parent;
                } else {
                    break;
                }
            }
        }

        // Internal: sift down from index
        fn siftDown(self: *Self, index: usize) void {
            var i = index;
            const half = self.len / 2;
            
            while (i < half) {
                var child = 2 * i + 1;
                const right = child + 1;
                
                if (right < self.len and self.compare(self.items[right], self.items[child]) == .lt) {
                    child = right;
                }
                
                if (self.compare(self.items[i], self.items[child]) != .gt) {
                    break;
                }
                
                self.swap(i, child);
                i = child;
            }
        }

        // Internal: swap two elements
        fn swap(self: *Self, a: usize, b: usize) void {
            const tmp = self.items[a];
            self.items[a] = self.items[b];
            self.items[b] = tmp;
        }
    };
}

/// Comparison function for min-heap (smaller values have higher priority)
pub fn minCompare(comptime T: type) fn (a: T, b: T) Order {
    return struct {
        fn compare(a: T, b: T) Order {
            return std.math.order(a, b);
        }
    }.compare;
}

/// Comparison function for max-heap (larger values have higher priority)
pub fn maxCompare(comptime T: type) fn (a: T, b: T) Order {
    return struct {
        fn compare(a: T, b: T) Order {
            return std.math.order(b, a);
        }
    }.compare;
}

/// Comparison for tuples (first element as priority)
pub fn tupleCompare(comptime T: type) fn (a: T, b: T) Order {
    return struct {
        fn compare(a: T, b: T) Order {
            return std.math.order(a[0], b[0]);
        }
    }.compare;
}

// Tests
test "PriorityQueue - basic min-heap operations" {
    const allocator = std.testing.allocator;
    
    var pq = PriorityQueue(i32).init(allocator, minCompare(i32));
    defer pq.deinit();
    
    try std.testing.expect(pq.isEmpty());
    try std.testing.expectEqual(@as(usize, 0), pq.count());
    try std.testing.expectEqual(@as(?i32, null), pq.peek());
    
    try pq.insert(5);
    try pq.insert(3);
    try pq.insert(7);
    try pq.insert(1);
    try pq.insert(9);
    
    try std.testing.expect(!pq.isEmpty());
    try std.testing.expectEqual(@as(usize, 5), pq.count());
    try std.testing.expectEqual(@as(i32, 1), pq.peek().?);
    
    // Should remove in ascending order for min-heap
    try std.testing.expectEqual(@as(i32, 1), pq.remove().?);
    try std.testing.expectEqual(@as(i32, 3), pq.remove().?);
    try std.testing.expectEqual(@as(i32, 5), pq.remove().?);
    try std.testing.expectEqual(@as(i32, 7), pq.remove().?);
    try std.testing.expectEqual(@as(i32, 9), pq.remove().?);
    try std.testing.expect(pq.isEmpty());
}

test "PriorityQueue - basic max-heap operations" {
    const allocator = std.testing.allocator;
    
    var pq = PriorityQueue(i32).init(allocator, maxCompare(i32));
    defer pq.deinit();
    
    try pq.insert(5);
    try pq.insert(3);
    try pq.insert(7);
    try pq.insert(1);
    try pq.insert(9);
    
    // Should remove in descending order for max-heap
    try std.testing.expectEqual(@as(i32, 9), pq.remove().?);
    try std.testing.expectEqual(@as(i32, 7), pq.remove().?);
    try std.testing.expectEqual(@as(i32, 5), pq.remove().?);
    try std.testing.expectEqual(@as(i32, 3), pq.remove().?);
    try std.testing.expectEqual(@as(i32, 1), pq.remove().?);
}

test "PriorityQueue - with capacity" {
    const allocator = std.testing.allocator;
    
    var pq = try PriorityQueue(i32).initCapacity(allocator, 10, minCompare(i32));
    defer pq.deinit();
    
    try std.testing.expectEqual(@as(usize, 10), pq.capacity);
    
    try pq.insert(1);
    try pq.insert(2);
    try std.testing.expectEqual(@as(usize, 2), pq.count());
}

test "PriorityQueue - clear operation" {
    const allocator = std.testing.allocator;
    
    var pq = PriorityQueue(i32).init(allocator, minCompare(i32));
    defer pq.deinit();
    
    try pq.insert(1);
    try pq.insert(2);
    try pq.insert(3);
    
    pq.clear();
    try std.testing.expect(pq.isEmpty());
    try std.testing.expectEqual(@as(usize, 0), pq.count());
}

test "PriorityQueue - dynamic growth" {
    const allocator = std.testing.allocator;
    
    var pq = PriorityQueue(i32).init(allocator, minCompare(i32));
    defer pq.deinit();
    
    // Insert many elements to test growth
    var i: i32 = 100;
    while (i > 0) : (i -= 1) {
        try pq.insert(i);
    }
    
    try std.testing.expectEqual(@as(usize, 100), pq.count());
    
    // Verify order
    i = 1;
    while (i <= 100) : (i += 1) {
        try std.testing.expectEqual(i, pq.remove().?);
    }
}

test "PriorityQueue - tuple priority" {
    const allocator = std.testing.allocator;
    const Tuple = struct { i32, []const u8 };
    
    var pq = PriorityQueue(Tuple).init(allocator, tupleCompare(Tuple));
    defer pq.deinit();
    
    try pq.insert(.{ 3, "low" });
    try pq.insert(.{ 1, "high" });
    try pq.insert(.{ 2, "medium" });
    
    const peeked = pq.peek().?;
    try std.testing.expectEqual(@as(i32, 1), peeked[0]);
    
    const first = pq.remove().?;
    try std.testing.expectEqual(@as(i32, 1), first[0]);
    try std.testing.expectEqualStrings("high", first[1]);
}

test "PriorityQueue - custom struct" {
    const allocator = std.testing.allocator;
    const Task = struct {
        priority: i32,
        name: []const u8,
    };
    
    const compare = struct {
        fn cmp(a: Task, b: Task) Order {
            return std.math.order(a.priority, b.priority);
        }
    }.cmp;
    
    var pq = PriorityQueue(Task).init(allocator, compare);
    defer pq.deinit();
    
    try pq.insert(.{ .priority = 10, .name = "low priority" });
    try pq.insert(.{ .priority = 1, .name = "high priority" });
    try pq.insert(.{ .priority = 5, .name = "medium priority" });
    
    const first = pq.remove().?;
    try std.testing.expectEqual(@as(i32, 1), first.priority);
    try std.testing.expectEqualStrings("high priority", first.name);
}