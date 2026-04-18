const std = @import("std");
const Allocator = std.mem.Allocator;

/// RingBuffer - A circular buffer implementation with fixed capacity.
/// Provides O(1) push and pop operations, efficient memory usage,
/// and thread-safe variants for concurrent access.
///
/// Features:
/// - Fixed capacity with efficient wrap-around
/// - Push operations with overflow handling
/// - Peek operations without removal
/// - Iterator support for reading all elements
/// - Slice access for bulk operations
/// - Memory-efficient storage
///
/// Example usage:
/// ```zig
/// var buffer = try RingBuffer(i32).init(allocator, 10);
/// defer buffer.deinit();
/// try buffer.push(42);
/// const value = buffer.pop();
/// ```
pub fn RingBuffer(comptime T: type) type {
    return struct {
        const Self = @This();

        buffer: []T,
        capacity: usize,
        head: usize,
        tail: usize,
        len: usize,
        allocator: Allocator,

        /// Initialize a new RingBuffer with given capacity
        pub fn init(allocator: Allocator, capacity: usize) !Self {
            if (capacity == 0) return error.ZeroCapacity;

            const buffer = try allocator.alloc(T, capacity);
            return Self{
                .buffer = buffer,
                .capacity = capacity,
                .head = 0,
                .tail = 0,
                .len = 0,
                .allocator = allocator,
            };
        }

        /// Free all allocated memory
        pub fn deinit(self: *Self) void {
            self.allocator.free(self.buffer);
            self.* = undefined;
        }

        /// Clear the buffer without freeing memory
        pub fn clear(self: *Self) void {
            self.head = 0;
            self.tail = 0;
            self.len = 0;
        }

        /// Push an item to the buffer
        /// Returns error.BufferFull if the buffer is at capacity
        pub fn push(self: *Self, item: T) !void {
            if (self.len >= self.capacity) return error.BufferFull;

            self.buffer[self.tail] = item;
            self.tail = (self.tail + 1) % self.capacity;
            self.len += 1;
        }

        /// Push an item, overwriting the oldest if full
        /// Returns true if an item was overwritten
        pub fn pushOverwrite(self: *Self, item: T) bool {
            const was_full = self.len >= self.capacity;

            if (was_full) {
                // Overwrite the oldest item
                self.head = (self.head + 1) % self.capacity;
            } else {
                self.len += 1;
            }

            self.buffer[self.tail] = item;
            self.tail = (self.tail + 1) % self.capacity;

            return was_full;
        }

        /// Pop an item from the buffer
        /// Returns null if the buffer is empty
        pub fn pop(self: *Self) ?T {
            if (self.len == 0) return null;

            const item = self.buffer[self.head];
            self.head = (self.head + 1) % self.capacity;
            self.len -= 1;
            return item;
        }

        /// Peek at the front item without removing it
        /// Returns null if the buffer is empty
        pub fn peek(self: *const Self) ?T {
            if (self.len == 0) return null;
            return self.buffer[self.head];
        }

        /// Peek at the back item without removing it
        /// Returns null if the buffer is empty
        pub fn peekBack(self: *const Self) ?T {
            if (self.len == 0) return null;
            const index = if (self.tail == 0) self.capacity - 1 else self.tail - 1;
            return self.buffer[index];
        }

        /// Peek at item at given index (0 = front)
        /// Returns null if index out of bounds
        pub fn peekAt(self: *const Self, index: usize) ?T {
            if (index >= self.len) return null;
            const actual_index = (self.head + index) % self.capacity;
            return self.buffer[actual_index];
        }

        /// Check if the buffer is empty
        pub fn isEmpty(self: *const Self) bool {
            return self.len == 0;
        }

        /// Check if the buffer is full
        pub fn isFull(self: *const Self) bool {
            return self.len >= self.capacity;
        }

        /// Get the current length
        pub fn length(self: *const Self) usize {
            return self.len;
        }

        /// Get the remaining capacity
        pub fn remaining(self: *const Self) usize {
            return self.capacity - self.len;
        }

        /// Push multiple items at once
        /// Returns the number of items actually pushed
        pub fn pushSlice(self: *Self, items: []const T) usize {
            var pushed: usize = 0;
            for (items) |item| {
                self.push(item) catch break;
                pushed += 1;
            }
            return pushed;
        }

        /// Pop multiple items into a slice
        /// Returns the number of items actually popped
        pub fn popSlice(self: *Self, dest: []T) usize {
            var popped: usize = 0;
            while (popped < dest.len) {
                const item = self.pop() orelse break;
                dest[popped] = item;
                popped += 1;
            }
            return popped;
        }

        /// Convert buffer contents to a slice
        /// Caller owns the allocated memory
        pub fn toSlice(self: *const Self, allocator: Allocator) ![]T {
            const result = try allocator.alloc(T, self.len);
            for (0..self.len) |i| {
                result[i] = self.peekAt(i).?;
            }
            return result;
        }

        /// Create an iterator over the buffer contents
        pub fn iterator(self: *const Self) Iterator(T) {
            return Iterator(T).init(self);
        }

        /// Check if an item is in the buffer (requires T to be comparable)
        pub fn contains(self: *const Self, item: T) bool {
            var iter = self.iterator();
            while (iter.next()) |v| {
                if (std.meta.eql(v, item)) return true;
            }
            return false;
        }

        /// Find the index of an item, or null if not found
        pub fn indexOf(self: *const Self, item: T) ?usize {
            for (0..self.len) |i| {
                if (std.meta.eql(self.peekAt(i).?, item)) {
                    return i;
                }
            }
            return null;
        }

        /// Remove item at index, shifting subsequent items
        /// Returns the removed item, or null if index invalid
        pub fn removeAt(self: *Self, index: usize) ?T {
            if (index >= self.len) return null;

            const actual_index = (self.head + index) % self.capacity;
            const item = self.buffer[actual_index];

            // Shift items after the removed one
            var i = index;
            while (i < self.len - 1) : (i += 1) {
                const curr = (self.head + i) % self.capacity;
                const next = (self.head + i + 1) % self.capacity;
                self.buffer[curr] = self.buffer[next];
            }

            self.tail = if (self.tail == 0) self.capacity - 1 else self.tail - 1;
            self.len -= 1;

            return item;
        }

        /// Get a view into the buffer as two slices (for zero-copy access)
        /// Useful when you need contiguous access to elements
        pub fn asSlices(self: *const Self) [2][]const T {
            if (self.len == 0) {
                return .{ &.{}, &.{} };
            }

            const first_len = if (self.tail > self.head)
                self.len
            else
                self.capacity - self.head;

            const actual_first_len = @min(first_len, self.len);
            return .{
                self.buffer[self.head .. self.head + actual_first_len],
                self.buffer[0 .. self.len - actual_first_len],
            };
        }
    };
}

/// Iterator for RingBuffer
pub fn Iterator(comptime T: type) type {
    return struct {
        buffer: *const RingBuffer(T),
        index: usize,

        pub fn init(buffer: *const RingBuffer(T)) @This() {
            return .{
                .buffer = buffer,
                .index = 0,
            };
        }

        pub fn next(self: *@This()) ?T {
            if (self.index >= self.buffer.len) return null;
            const item = self.buffer.peekAt(self.index).?;
            self.index += 1;
            return item;
        }

        pub fn reset(self: *@This()) void {
            self.index = 0;
        }
    };
}

/// BoundedRingBuffer - A ring buffer with max capacity that can grow dynamically
/// up to a maximum size. Uses a slice allocator pattern.
pub fn BoundedRingBuffer(comptime T: type) type {
    return struct {
        const Self = @This();

        buffer: []T,
        capacity: usize,
        max_capacity: usize,
        head: usize,
        tail: usize,
        len: usize,
        allocator: Allocator,

        pub fn init(allocator: Allocator, initial_capacity: usize, max_capacity: usize) !Self {
            if (initial_capacity == 0) return error.ZeroCapacity;
            if (max_capacity < initial_capacity) return error.InvalidCapacity;

            const buffer = try allocator.alloc(T, initial_capacity);
            return Self{
                .buffer = buffer,
                .capacity = initial_capacity,
                .max_capacity = max_capacity,
                .head = 0,
                .tail = 0,
                .len = 0,
                .allocator = allocator,
            };
        }

        pub fn deinit(self: *Self) void {
            self.allocator.free(self.buffer);
        }

        pub fn push(self: *Self, item: T) !void {
            // Try to grow if at capacity
            if (self.len >= self.capacity) {
                if (self.capacity < self.max_capacity) {
                    try self.grow();
                } else {
                    return error.BufferFull;
                }
            }

            self.buffer[self.tail] = item;
            self.tail = (self.tail + 1) % self.capacity;
            self.len += 1;
        }

        fn grow(self: *Self) !void {
            const new_capacity = @min(self.capacity * 2, self.max_capacity);
            if (new_capacity == self.capacity) return error.BufferFull;

            const new_buffer = try self.allocator.alloc(T, new_capacity);
            errdefer self.allocator.free(new_buffer);

            // Copy elements
            for (0..self.len) |i| {
                new_buffer[i] = self.peekAt(i).?;
            }

            self.allocator.free(self.buffer);
            self.buffer = new_buffer;
            self.capacity = new_capacity;
            self.head = 0;
            self.tail = self.len;
        }

        pub fn pop(self: *Self) ?T {
            if (self.len == 0) return null;

            const item = self.buffer[self.head];
            self.head = (self.head + 1) % self.capacity;
            self.len -= 1;
            return item;
        }

        pub fn peek(self: *const Self) ?T {
            if (self.len == 0) return null;
            return self.buffer[self.head];
        }

        pub fn peekAt(self: *const Self, index: usize) ?T {
            if (index >= self.len) return null;
            const actual_index = (self.head + index) % self.capacity;
            return self.buffer[actual_index];
        }

        pub fn length(self: *const Self) usize {
            return self.len;
        }

        pub fn isEmpty(self: *const Self) bool {
            return self.len == 0;
        }

        pub fn isFull(self: *const Self) bool {
            return self.len >= self.capacity;
        }

        /// Check if at maximum capacity (cannot grow further)
        pub fn atMaxCapacity(self: *const Self) bool {
            return self.capacity >= self.max_capacity;
        }
    };
}

/// AtomicRingBuffer - A thread-safe ring buffer using mutex
pub fn AtomicRingBuffer(comptime T: type) type {
    return struct {
        const Self = @This();

        buffer: []T,
        capacity: usize,
        head: usize,
        tail: usize,
        len: usize,
        allocator: Allocator,
        mutex: std.Thread.Mutex,

        pub fn init(allocator: Allocator, capacity: usize) !Self {
            if (capacity == 0) return error.ZeroCapacity;

            const buffer = try allocator.alloc(T, capacity);
            return Self{
                .buffer = buffer,
                .capacity = capacity,
                .head = 0,
                .tail = 0,
                .len = 0,
                .allocator = allocator,
                .mutex = std.Thread.Mutex{},
            };
        }

        pub fn deinit(self: *Self) void {
            self.allocator.free(self.buffer);
        }

        pub fn push(self: *Self, item: T) !void {
            self.mutex.lock();
            defer self.mutex.unlock();

            if (self.len >= self.capacity) return error.BufferFull;

            self.buffer[self.tail] = item;
            self.tail = (self.tail + 1) % self.capacity;
            self.len += 1;
        }

        pub fn pop(self: *Self) ?T {
            self.mutex.lock();
            defer self.mutex.unlock();

            if (self.len == 0) return null;

            const item = self.buffer[self.head];
            self.head = (self.head + 1) % self.capacity;
            self.len -= 1;
            return item;
        }

        pub fn length(self: *Self) usize {
            self.mutex.lock();
            defer self.mutex.unlock();
            return self.len;
        }

        pub fn isEmpty(self: *Self) bool {
            self.mutex.lock();
            defer self.mutex.unlock();
            return self.len == 0;
        }

        pub fn isFull(self: *Self) bool {
            self.mutex.lock();
            defer self.mutex.unlock();
            return self.len >= self.capacity;
        }
    };
}

// ============================================
// Unit Tests
// ============================================

test "RingBuffer - basic push and pop" {
    const allocator = std.testing.allocator;

    var buffer = try RingBuffer(i32).init(allocator, 5);
    defer buffer.deinit();

    try buffer.push(1);
    try buffer.push(2);
    try buffer.push(3);

    try std.testing.expectEqual(@as(usize, 3), buffer.length());
    try std.testing.expectEqual(@as(usize, 2), buffer.remaining());

    try std.testing.expectEqual(@as(i32, 1), buffer.pop().?);
    try std.testing.expectEqual(@as(i32, 2), buffer.pop().?);
    try std.testing.expectEqual(@as(i32, 3), buffer.pop().?);
    try std.testing.expectEqual(@as(?i32, null), buffer.pop());
    try std.testing.expect(buffer.isEmpty());
}

test "RingBuffer - pushOverwrite" {
    const allocator = std.testing.allocator;

    var buffer = try RingBuffer(i32).init(allocator, 3);
    defer buffer.deinit();

    _ = buffer.pushOverwrite(1);
    _ = buffer.pushOverwrite(2);
    _ = buffer.pushOverwrite(3);
    try std.testing.expect(buffer.isFull());

    // Should overwrite oldest
    const overwritten = buffer.pushOverwrite(4);
    try std.testing.expect(overwritten);

    try std.testing.expectEqual(@as(i32, 2), buffer.pop().?);
    try std.testing.expectEqual(@as(i32, 3), buffer.pop().?);
    try std.testing.expectEqual(@as(i32, 4), buffer.pop().?);
}

test "RingBuffer - peek operations" {
    const allocator = std.testing.allocator;

    var buffer = try RingBuffer(i32).init(allocator, 5);
    defer buffer.deinit();

    try std.testing.expectEqual(@as(?i32, null), buffer.peek());
    try std.testing.expectEqual(@as(?i32, null), buffer.peekBack());

    try buffer.push(10);
    try buffer.push(20);
    try buffer.push(30);

    try std.testing.expectEqual(@as(i32, 10), buffer.peek().?);
    try std.testing.expectEqual(@as(i32, 30), buffer.peekBack().?);
    try std.testing.expectEqual(@as(i32, 20), buffer.peekAt(1).?);
    try std.testing.expectEqual(@as(?i32, null), buffer.peekAt(10));

    // Peek doesn't modify the buffer
    try std.testing.expectEqual(@as(usize, 3), buffer.length());
}

test "RingBuffer - wrap around" {
    const allocator = std.testing.allocator;

    var buffer = try RingBuffer(i32).init(allocator, 3);
    defer buffer.deinit();

    // Fill and empty multiple times
    for (0..3) |_| {
        try buffer.push(1);
        try buffer.push(2);
        try buffer.push(3);

        try std.testing.expectEqual(@as(i32, 1), buffer.pop().?);
        try std.testing.expectEqual(@as(i32, 2), buffer.pop().?);
        try std.testing.expectEqual(@as(i32, 3), buffer.pop().?);
        try std.testing.expect(buffer.isEmpty());
    }
}

test "RingBuffer - pushSlice and popSlice" {
    const allocator = std.testing.allocator;

    var buffer = try RingBuffer(i32).init(allocator, 10);
    defer buffer.deinit();

    const items = [_]i32{ 1, 2, 3, 4, 5 };
    const pushed = buffer.pushSlice(&items);
    try std.testing.expectEqual(@as(usize, 5), pushed);

    var dest: [3]i32 = undefined;
    const popped = buffer.popSlice(&dest);
    try std.testing.expectEqual(@as(usize, 3), popped);
    try std.testing.expectEqualSlices(i32, &[_]i32{ 1, 2, 3 }, &dest);
}

test "RingBuffer - toSlice" {
    const allocator = std.testing.allocator;

    var buffer = try RingBuffer(i32).init(allocator, 5);
    defer buffer.deinit();

    try buffer.push(10);
    try buffer.push(20);
    try buffer.push(30);

    const slice = try buffer.toSlice(allocator);
    defer allocator.free(slice);

    try std.testing.expectEqualSlices(i32, &[_]i32{ 10, 20, 30 }, slice);
}

test "RingBuffer - contains and indexOf" {
    const allocator = std.testing.allocator;

    var buffer = try RingBuffer(i32).init(allocator, 5);
    defer buffer.deinit();

    try buffer.push(1);
    try buffer.push(2);
    try buffer.push(3);

    try std.testing.expect(buffer.contains(2));
    try std.testing.expect(!buffer.contains(5));

    try std.testing.expectEqual(@as(usize, 0), buffer.indexOf(1).?);
    try std.testing.expectEqual(@as(usize, 2), buffer.indexOf(3).?);
    try std.testing.expectEqual(@as(?usize, null), buffer.indexOf(99));
}

test "RingBuffer - removeAt" {
    const allocator = std.testing.allocator;

    var buffer = try RingBuffer(i32).init(allocator, 5);
    defer buffer.deinit();

    try buffer.push(1);
    try buffer.push(2);
    try buffer.push(3);
    try buffer.push(4);

    const removed = buffer.removeAt(1);
    try std.testing.expectEqual(@as(i32, 2), removed.?);
    try std.testing.expectEqual(@as(usize, 3), buffer.length());

    try std.testing.expectEqual(@as(i32, 1), buffer.pop().?);
    try std.testing.expectEqual(@as(i32, 3), buffer.pop().?);
    try std.testing.expectEqual(@as(i32, 4), buffer.pop().?);
}

test "RingBuffer - asSlices" {
    const allocator = std.testing.allocator;

    var buffer = try RingBuffer(i32).init(allocator, 5);
    defer buffer.deinit();

    try buffer.push(1);
    try buffer.push(2);
    try buffer.push(3);

    const slices = buffer.asSlices();
    try std.testing.expectEqualSlices(i32, &[_]i32{ 1, 2, 3 }, slices[0]);
    try std.testing.expectEqual(@as(usize, 0), slices[1].len);
}

test "RingBuffer - clear" {
    const allocator = std.testing.allocator;

    var buffer = try RingBuffer(i32).init(allocator, 5);
    defer buffer.deinit();

    try buffer.push(1);
    try buffer.push(2);
    try buffer.push(3);

    buffer.clear();
    try std.testing.expect(buffer.isEmpty());
    try std.testing.expectEqual(@as(usize, 0), buffer.length());
}

test "RingBuffer - buffer full error" {
    const allocator = std.testing.allocator;

    var buffer = try RingBuffer(i32).init(allocator, 2);
    defer buffer.deinit();

    try buffer.push(1);
    try buffer.push(2);

    const result = buffer.push(3);
    try std.testing.expectError(error.BufferFull, result);
}

test "RingBuffer - zero capacity error" {
    const allocator = std.testing.allocator;

    const result = RingBuffer(i32).init(allocator, 0);
    try std.testing.expectError(error.ZeroCapacity, result);
}

test "RingBuffer - iterator" {
    const allocator = std.testing.allocator;

    var buffer = try RingBuffer(i32).init(allocator, 5);
    defer buffer.deinit();

    try buffer.push(10);
    try buffer.push(20);
    try buffer.push(30);

    var iter = buffer.iterator();
    try std.testing.expectEqual(@as(i32, 10), iter.next().?);
    try std.testing.expectEqual(@as(i32, 20), iter.next().?);
    try std.testing.expectEqual(@as(i32, 30), iter.next().?);
    try std.testing.expectEqual(@as(?i32, null), iter.next());

    // Reset and iterate again
    iter.reset();
    try std.testing.expectEqual(@as(i32, 10), iter.next().?);
}

test "RingBuffer - with strings" {
    const allocator = std.testing.allocator;

    var buffer = try RingBuffer([]const u8).init(allocator, 3);
    defer buffer.deinit();

    try buffer.push("hello");
    try buffer.push("world");
    try buffer.push("zig");

    try std.testing.expectEqualSlices(u8, "hello", buffer.pop().?);
    try std.testing.expectEqualSlices(u8, "world", buffer.pop().?);
}

test "BoundedRingBuffer - basic operations" {
    const allocator = std.testing.allocator;

    var buffer = try BoundedRingBuffer(i32).init(allocator, 2, 8);
    defer buffer.deinit();

    try buffer.push(1);
    try buffer.push(2);
    try std.testing.expect(buffer.isFull());

    // Should auto-grow
    try buffer.push(3);
    try buffer.push(4);
    try buffer.push(5);

    try std.testing.expectEqual(@as(usize, 5), buffer.length());
}

test "AtomicRingBuffer - thread safety" {
    const allocator = std.testing.allocator;

    var buffer = try AtomicRingBuffer(i32).init(allocator, 100);
    defer buffer.deinit();

    // Basic test
    try buffer.push(1);
    try buffer.push(2);
    try buffer.push(3);

    try std.testing.expectEqual(@as(usize, 3), buffer.length());
    try std.testing.expectEqual(@as(i32, 1), buffer.pop().?);
    try std.testing.expectEqual(@as(i32, 2), buffer.pop().?);
    try std.testing.expectEqual(@as(i32, 3), buffer.pop().?);
    try std.testing.expect(buffer.isEmpty());
}

test "RingBuffer - large data stress test" {
    const allocator = std.testing.allocator;

    var buffer = try RingBuffer(i32).init(allocator, 1000);
    defer buffer.deinit();

    // Fill
    for (0..1000) |i| {
        try buffer.push(@intCast(i));
    }
    try std.testing.expect(buffer.isFull());

    // Empty and verify
    for (0..1000) |i| {
        const val = buffer.pop().?;
        try std.testing.expectEqual(@as(i32, @intCast(i)), val);
    }
    try std.testing.expect(buffer.isEmpty());
}