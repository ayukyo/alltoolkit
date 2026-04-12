const std = @import("std");
const mem = std.mem;

/// Error types for data structure operations
pub const DataStructureError = error{
    /// The data structure is empty
    Empty,
    /// The requested item was not found
    NotFound,
    /// Index out of bounds
    IndexOutOfBounds,
    /// Buffer capacity exceeded
    CapacityExceeded,
    /// Memory allocation failed
    OutOfMemory,
    /// Invalid operation for current state
    InvalidOperation,
};

// ============================================================================
// STACK (LIFO - Last In, First Out)
// ============================================================================

/// A generic stack (LIFO) implementation using a dynamic array.
/// 
/// Supports O(1) push and pop operations with automatic resizing.
pub fn Stack(comptime T: type) type {
    return struct {
        const Self = @This();
        
        items: []T,
        capacity: usize,
        allocator: mem.Allocator,

        /// Create a new empty stack
        pub fn init(allocator: mem.Allocator) Self {
            return .{
                .items = &[_]T{},
                .capacity = 0,
                .allocator = allocator,
            };
        }

        /// Create a new stack with initial capacity
        pub fn initWithCapacity(allocator: mem.Allocator, initial_capacity: usize) mem.Allocator.Error!Self {
            if (initial_capacity == 0) {
                return init(allocator);
            }
            const items = try allocator.alloc(T, initial_capacity);
            return .{
                .items = items[0..0],
                .capacity = initial_capacity,
                .allocator = allocator,
            };
        }

        /// Free all allocated memory
        pub fn deinit(self: *Self) void {
            if (self.capacity > 0) {
                self.allocator.free(self.items.ptr[0..self.capacity]);
            }
        }

        /// Push an item onto the stack
        pub fn push(self: *Self, item: T) mem.Allocator.Error!void {
            if (self.items.len >= self.capacity) {
                try self.grow();
            }
            self.items.ptr[self.items.len] = item;
            self.items.len += 1;
        }

        /// Pop an item from the stack
        pub fn pop(self: *Self) ?T {
            if (self.items.len == 0) return null;
            self.items.len -= 1;
            return self.items.ptr[self.items.len];
        }

        /// Peek at the top item without removing it
        pub fn peek(self: *const Self) ?T {
            if (self.items.len == 0) return null;
            return self.items.ptr[self.items.len - 1];
        }

        /// Get current size
        pub fn len(self: *const Self) usize {
            return self.items.len;
        }

        /// Check if stack is empty
        pub fn isEmpty(self: *const Self) bool {
            return self.items.len == 0;
        }

        /// Clear all items (does not free memory)
        pub fn clear(self: *Self) void {
            self.items.len = 0;
        }

        /// Convert to owned slice (caller owns the memory)
        pub fn toOwnedSlice(self: *Self) mem.Allocator.Error![]T {
            const result = try self.allocator.dupe(T, self.items);
            self.clear();
            return result;
        }

        fn grow(self: *Self) mem.Allocator.Error!void {
            const new_capacity = if (self.capacity == 0) 4 else self.capacity * 2;
            const new_items = try self.allocator.alloc(T, new_capacity);
            
            @memcpy(new_items[0..self.items.len], self.items);
            
            if (self.capacity > 0) {
                self.allocator.free(self.items.ptr[0..self.capacity]);
            }
            
            self.items = new_items[0..self.items.len];
            self.items.ptr = new_items.ptr;
            self.capacity = new_capacity;
        }
    };
}

// ============================================================================
// QUEUE (FIFO - First In, First Out)
// ============================================================================

/// A generic queue (FIFO) implementation using a ring buffer.
/// 
/// Supports O(1) enqueue and dequeue operations with automatic resizing.
pub fn Queue(comptime T: type) type {
    return struct {
        const Self = @This();
        
        buffer: []T,
        head: usize,
        tail: usize,
        count: usize,
        allocator: mem.Allocator,

        /// Create a new empty queue
        pub fn init(allocator: mem.Allocator) Self {
            return .{
                .buffer = &[_]T{},
                .head = 0,
                .tail = 0,
                .count = 0,
                .allocator = allocator,
            };
        }

        /// Create a new queue with initial capacity
        pub fn initWithCapacity(allocator: mem.Allocator, initial_capacity: usize) mem.Allocator.Error!Self {
            if (initial_capacity == 0) {
                return init(allocator);
            }
            const buffer = try allocator.alloc(T, initial_capacity);
            return .{
                .buffer = buffer,
                .head = 0,
                .tail = 0,
                .count = 0,
                .allocator = allocator,
            };
        }

        /// Free all allocated memory
        pub fn deinit(self: *Self) void {
            if (self.buffer.len > 0) {
                self.allocator.free(self.buffer);
            }
        }

        /// Add an item to the back of the queue
        pub fn enqueue(self: *Self, item: T) mem.Allocator.Error!void {
            if (self.count >= self.buffer.len) {
                try self.grow();
            }
            self.buffer[self.tail] = item;
            self.tail = (self.tail + 1) % self.buffer.len;
            self.count += 1;
        }

        /// Remove and return the front item
        pub fn dequeue(self: *Self) ?T {
            if (self.count == 0) return null;
            const item = self.buffer[self.head];
            self.head = (self.head + 1) % self.buffer.len;
            self.count -= 1;
            return item;
        }

        /// Peek at the front item without removing it
        pub fn peek(self: *const Self) ?T {
            if (self.count == 0) return null;
            return self.buffer[self.head];
        }

        /// Get current size
        pub fn len(self: *const Self) usize {
            return self.count;
        }

        /// Check if queue is empty
        pub fn isEmpty(self: *const Self) bool {
            return self.count == 0;
        }

        /// Clear all items
        pub fn clear(self: *Self) void {
            self.head = 0;
            self.tail = 0;
            self.count = 0;
        }

        fn grow(self: *Self) mem.Allocator.Error!void {
            const new_capacity = if (self.buffer.len == 0) 4 else self.buffer.len * 2;
            const new_buffer = try self.allocator.alloc(T, new_capacity);
            
            // Copy items in order
            if (self.count > 0) {
                if (self.head < self.tail) {
                    @memcpy(new_buffer[0..self.count], self.buffer[self.head..self.tail]);
                } else {
                    const first_part = self.buffer[self.head..];
                    const second_part = self.buffer[0..self.tail];
                    @memcpy(new_buffer[0..first_part.len], first_part);
                    @memcpy(new_buffer[first_part.len..][0..second_part.len], second_part);
                }
            }
            
            if (self.buffer.len > 0) {
                self.allocator.free(self.buffer);
            }
            
            self.buffer = new_buffer;
            self.head = 0;
            self.tail = self.count;
        }
    };
}

// ============================================================================
// LINKED LIST
// ============================================================================

/// A generic doubly-linked list implementation.
pub fn LinkedList(comptime T: type) type {
    return struct {
        const Self = @This();
        
        /// Node in the linked list
        pub const Node = struct {
            data: T,
            prev: ?*Node,
            next: ?*Node,
        };

        head: ?*Node,
        tail: ?*Node,
        count: usize,
        allocator: mem.Allocator,

        /// Create a new empty linked list
        pub fn init(allocator: mem.Allocator) Self {
            return .{
                .head = null,
                .tail = null,
                .count = 0,
                .allocator = allocator,
            };
        }

        /// Free all nodes
        pub fn deinit(self: *Self) void {
            var current = self.head;
            while (current) |node| {
                const next = node.next;
                self.allocator.destroy(node);
                current = next;
            }
        }

        /// Add item to the front
        pub fn pushFront(self: *Self, item: T) mem.Allocator.Error!void {
            const node = try self.allocator.create(Node);
            node.* = .{
                .data = item,
                .prev = null,
                .next = self.head,
            };
            
            if (self.head) |head| {
                head.prev = node;
            } else {
                self.tail = node;
            }
            self.head = node;
            self.count += 1;
        }

        /// Add item to the back
        pub fn pushBack(self: *Self, item: T) mem.Allocator.Error!void {
            const node = try self.allocator.create(Node);
            node.* = .{
                .data = item,
                .prev = self.tail,
                .next = null,
            };
            
            if (self.tail) |tail| {
                tail.next = node;
            } else {
                self.head = node;
            }
            self.tail = node;
            self.count += 1;
        }

        /// Remove and return the front item
        pub fn popFront(self: *Self) ?T {
            const head = self.head orelse return null;
            const data = head.data;
            
            self.head = head.next;
            if (self.head) |new_head| {
                new_head.prev = null;
            } else {
                self.tail = null;
            }
            
            self.allocator.destroy(head);
            self.count -= 1;
            return data;
        }

        /// Remove and return the back item
        pub fn popBack(self: *Self) ?T {
            const tail = self.tail orelse return null;
            const data = tail.data;
            
            self.tail = tail.prev;
            if (self.tail) |new_tail| {
                new_tail.next = null;
            } else {
                self.head = null;
            }
            
            self.allocator.destroy(tail);
            self.count -= 1;
            return data;
        }

        /// Peek at the front item
        pub fn peekFront(self: *const Self) ?T {
            return if (self.head) |head| head.data else null;
        }

        /// Peek at the back item
        pub fn peekBack(self: *const Self) ?T {
            return if (self.tail) |tail| tail.data else null;
        }

        /// Get current size
        pub fn len(self: *const Self) usize {
            return self.count;
        }

        /// Check if empty
        pub fn isEmpty(self: *const Self) bool {
            return self.count == 0;
        }

        /// Iterator for the linked list
        pub const Iterator = struct {
            current: ?*Node,

            pub fn next(self: *Iterator) ?T {
                const node = self.current orelse return null;
                self.current = node.next;
                return node.data;
            }
        };

        /// Get forward iterator
        pub fn iterator(self: *const Self) Iterator {
            return .{ .current = self.head };
        }

        /// Find an item (returns index or null)
        pub fn indexOf(self: *const Self, item: T) ?usize {
            var current = self.head;
            var idx: usize = 0;
            while (current) |node| {
                if (std.meta.eql(node.data, item)) return idx;
                current = node.next;
                idx += 1;
            }
            return null;
        }

        /// Remove first occurrence of an item
        pub fn remove(self: *Self, item: T) bool {
            var current = self.head;
            while (current) |node| {
                if (std.meta.eql(node.data, item)) {
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
                    self.allocator.destroy(node);
                    self.count -= 1;
                    return true;
                }
                current = node.next;
            }
            return false;
        }
    };
}

// ============================================================================
// DEQUE (Double-Ended Queue)
// ============================================================================

/// A generic double-ended queue implementation.
/// Supports efficient insertion and removal at both ends.
pub fn Deque(comptime T: type) type {
    return struct {
        const Self = @This();
        
        buffer: []T,
        head: usize,
        count: usize,
        allocator: mem.Allocator,

        /// Create a new empty deque
        pub fn init(allocator: mem.Allocator) Self {
            return .{
                .buffer = &[_]T{},
                .head = 0,
                .count = 0,
                .allocator = allocator,
            };
        }

        /// Create a new deque with initial capacity
        pub fn initWithCapacity(allocator: mem.Allocator, initial_capacity: usize) mem.Allocator.Error!Self {
            if (initial_capacity == 0) {
                return init(allocator);
            }
            const buffer = try allocator.alloc(T, initial_capacity);
            return .{
                .buffer = buffer,
                .head = 0,
                .count = 0,
                .allocator = allocator,
            };
        }

        /// Free all allocated memory
        pub fn deinit(self: *Self) void {
            if (self.buffer.len > 0) {
                self.allocator.free(self.buffer);
            }
        }

        /// Add item to the front
        pub fn pushFront(self: *Self, item: T) mem.Allocator.Error!void {
            if (self.count >= self.buffer.len) {
                try self.grow();
            }
            self.head = if (self.head == 0) self.buffer.len - 1 else self.head - 1;
            self.buffer[self.head] = item;
            self.count += 1;
        }

        /// Add item to the back
        pub fn pushBack(self: *Self, item: T) mem.Allocator.Error!void {
            if (self.count >= self.buffer.len) {
                try self.grow();
            }
            const tail = (self.head + self.count) % self.buffer.len;
            self.buffer[tail] = item;
            self.count += 1;
        }

        /// Remove and return the front item
        pub fn popFront(self: *Self) ?T {
            if (self.count == 0) return null;
            const item = self.buffer[self.head];
            self.head = (self.head + 1) % self.buffer.len;
            self.count -= 1;
            return item;
        }

        /// Remove and return the back item
        pub fn popBack(self: *Self) ?T {
            if (self.count == 0) return null;
            self.count -= 1;
            const tail = (self.head + self.count) % self.buffer.len;
            return self.buffer[tail];
        }

        /// Peek at the front item
        pub fn peekFront(self: *const Self) ?T {
            if (self.count == 0) return null;
            return self.buffer[self.head];
        }

        /// Peek at the back item
        pub fn peekBack(self: *const Self) ?T {
            if (self.count == 0) return null;
            const tail = (self.head + self.count - 1) % self.buffer.len;
            return self.buffer[tail];
        }

        /// Get item at index
        pub fn get(self: *const Self, index: usize) ?T {
            if (index >= self.count) return null;
            const actual_index = (self.head + index) % self.buffer.len;
            return self.buffer[actual_index];
        }

        /// Get current size
        pub fn len(self: *const Self) usize {
            return self.count;
        }

        /// Check if empty
        pub fn isEmpty(self: *const Self) bool {
            return self.count == 0;
        }

        /// Clear all items
        pub fn clear(self: *Self) void {
            self.head = 0;
            self.count = 0;
        }

        fn grow(self: *Self) mem.Allocator.Error!void {
            const new_capacity = if (self.buffer.len == 0) 4 else self.buffer.len * 2;
            const new_buffer = try self.allocator.alloc(T, new_capacity);
            
            if (self.count > 0) {
                for (0..self.count) |i| {
                    const src_idx = (self.head + i) % self.buffer.len;
                    new_buffer[i] = self.buffer[src_idx];
                }
            }
            
            if (self.buffer.len > 0) {
                self.allocator.free(self.buffer);
            }
            
            self.buffer = new_buffer;
            self.head = 0;
        }
    };
}

// ============================================================================
// PRIORITY QUEUE (Binary Heap)
// ============================================================================

/// A generic priority queue implementation using a binary heap.
/// By default, it's a max-heap. Use `comptime is_min_heap: bool = true` for min-heap.
pub fn PriorityQueue(comptime T: type, comptime is_min_heap: bool) type {
    return struct {
        const Self = @This();
        
        items: []T,
        capacity: usize,
        allocator: mem.Allocator,

        /// Create a new empty priority queue
        pub fn init(allocator: mem.Allocator) Self {
            return .{
                .items = &[_]T{},
                .capacity = 0,
                .allocator = allocator,
            };
        }

        /// Create with initial capacity
        pub fn initWithCapacity(allocator: mem.Allocator, initial_capacity: usize) mem.Allocator.Error!Self {
            if (initial_capacity == 0) {
                return init(allocator);
            }
            const items = try allocator.alloc(T, initial_capacity);
            return .{
                .items = items[0..0],
                .capacity = initial_capacity,
                .allocator = allocator,
            };
        }

        /// Free all memory
        pub fn deinit(self: *Self) void {
            if (self.capacity > 0) {
                self.allocator.free(self.items.ptr[0..self.capacity]);
            }
        }

        /// Insert an item
        pub fn insert(self: *Self, item: T) mem.Allocator.Error!void {
            if (self.items.len >= self.capacity) {
                try self.grow();
            }
            self.items.ptr[self.items.len] = item;
            self.items.len += 1;
            self.siftUp(self.items.len - 1);
        }

        /// Remove and return the top item
        pub fn pop(self: *Self) ?T {
            if (self.items.len == 0) return null;
            const result = self.items.ptr[0];
            self.items.len -= 1;
            if (self.items.len > 0) {
                self.items.ptr[0] = self.items.ptr[self.items.len];
                self.siftDown(0);
            }
            return result;
        }

        /// Peek at the top item
        pub fn peek(self: *const Self) ?T {
            if (self.items.len == 0) return null;
            return self.items.ptr[0];
        }

        /// Get current size
        pub fn len(self: *const Self) usize {
            return self.items.len;
        }

        /// Check if empty
        pub fn isEmpty(self: *const Self) bool {
            return self.items.len == 0;
        }

        /// Clear all items
        pub fn clear(self: *Self) void {
            self.items.len = 0;
        }

        fn compare(_: *const Self, a: T, b: T) bool {
            if (is_min_heap) {
                return a < b;
            } else {
                return a > b;
            }
        }

        fn siftUp(self: *Self, index: usize) void {
            var i = index;
            while (i > 0) {
                const parent = (i - 1) / 2;
                if (self.compare(self.items.ptr[i], self.items.ptr[parent])) {
                    self.swap(i, parent);
                    i = parent;
                } else {
                    break;
                }
            }
        }

        fn siftDown(self: *Self, index: usize) void {
            var i = index;
            while (true) {
                const left = 2 * i + 1;
                const right = 2 * i + 2;
                var target = i;

                if (left < self.items.len and self.compare(self.items.ptr[left], self.items.ptr[target])) {
                    target = left;
                }
                if (right < self.items.len and self.compare(self.items.ptr[right], self.items.ptr[target])) {
                    target = right;
                }

                if (target != i) {
                    self.swap(i, target);
                    i = target;
                } else {
                    break;
                }
            }
        }

        fn swap(self: *Self, a: usize, b: usize) void {
            const tmp = self.items.ptr[a];
            self.items.ptr[a] = self.items.ptr[b];
            self.items.ptr[b] = tmp;
        }

        fn grow(self: *Self) mem.Allocator.Error!void {
            const new_capacity = if (self.capacity == 0) 4 else self.capacity * 2;
            const new_items = try self.allocator.alloc(T, new_capacity);
            
            @memcpy(new_items[0..self.items.len], self.items);
            
            if (self.capacity > 0) {
                self.allocator.free(self.items.ptr[0..self.capacity]);
            }
            
            self.items = new_items[0..self.items.len];
            self.items.ptr = new_items.ptr;
            self.capacity = new_capacity;
        }
    };
}

// ============================================================================
// SET (Hash Set)
// ============================================================================

/// A simple hash set implementation using Zig's built-in HashMap.
pub fn HashSet(comptime T: type) type {
    return struct {
        const Self = @This();
        
        map: std.AutoHashMap(T, void),
        allocator: mem.Allocator,

        /// Create a new empty set
        pub fn init(allocator: mem.Allocator) Self {
            return .{
                .map = std.AutoHashMap(T, void).init(allocator),
                .allocator = allocator,
            };
        }

        /// Free all memory
        pub fn deinit(self: *Self) void {
            self.map.deinit();
        }

        /// Insert an item (returns true if newly inserted)
        pub fn insert(self: *Self, item: T) mem.Allocator.Error!bool {
            const gop = try self.map.getOrPut(item);
            return !gop.found_existing;
        }

        /// Remove an item (returns true if it existed)
        pub fn remove(self: *Self, item: T) bool {
            return self.map.remove(item);
        }

        /// Check if item exists
        pub fn contains(self: *const Self, item: T) bool {
            return self.map.contains(item);
        }

        /// Get current size
        pub fn len(self: *const Self) usize {
            return self.map.count();
        }

        /// Check if empty
        pub fn isEmpty(self: *const Self) bool {
            return self.map.count() == 0;
        }

        /// Clear all items
        pub fn clear(self: *Self) void {
            self.map.clearRetainingCapacity();
        }

        /// Iterator
        pub const Iterator = struct {
            map_iter: std.AutoHashMap(T, void).Iterator,

            pub fn next(self: *Iterator) ?T {
                const entry = self.map_iter.next() orelse return null;
                return entry.key_ptr.*;
            }
        };

        /// Get iterator
        pub fn iterator(self: *Self) Iterator {
            return .{ .map_iter = self.map.iterator() };
        }
    };
}

// ============================================================================
// TESTS
// ============================================================================

test "Stack - basic operations" {
    const allocator = std.testing.allocator;
    var stack = Stack(i32).init(allocator);
    defer stack.deinit();

    try std.testing.expect(stack.isEmpty());
    try std.testing.expectEqual(@as(usize, 0), stack.len());

    try stack.push(1);
    try stack.push(2);
    try stack.push(3);

    try std.testing.expect(!stack.isEmpty());
    try std.testing.expectEqual(@as(usize, 3), stack.len());
    try std.testing.expectEqual(@as(i32, 3), stack.peek());

    try std.testing.expectEqual(@as(i32, 3), stack.pop());
    try std.testing.expectEqual(@as(i32, 2), stack.pop());
    try std.testing.expectEqual(@as(i32, 1), stack.pop());
    try std.testing.expect(stack.isEmpty());
    try std.testing.expectEqual(@as(?i32, null), stack.pop());
}

test "Stack - with initial capacity" {
    const allocator = std.testing.allocator;
    var stack = try Stack(i32).initWithCapacity(allocator, 10);
    defer stack.deinit();

    for (0..20) |i| {
        try stack.push(@intCast(i));
    }

    try std.testing.expectEqual(@as(usize, 20), stack.len());
    try std.testing.expectEqual(@as(i32, 19), stack.peek());
}

test "Stack - clear and reuse" {
    const allocator = std.testing.allocator;
    var stack = Stack(i32).init(allocator);
    defer stack.deinit();

    try stack.push(1);
    try stack.push(2);
    stack.clear();

    try std.testing.expect(stack.isEmpty());
    try std.testing.expectEqual(@as(usize, 0), stack.len());

    try stack.push(3);
    try std.testing.expectEqual(@as(i32, 3), stack.pop());
}

test "Queue - basic operations" {
    const allocator = std.testing.allocator;
    var queue = Queue(i32).init(allocator);
    defer queue.deinit();

    try std.testing.expect(queue.isEmpty());

    try queue.enqueue(1);
    try queue.enqueue(2);
    try queue.enqueue(3);

    try std.testing.expect(!queue.isEmpty());
    try std.testing.expectEqual(@as(usize, 3), queue.len());
    try std.testing.expectEqual(@as(i32, 1), queue.peek());

    try std.testing.expectEqual(@as(i32, 1), queue.dequeue());
    try std.testing.expectEqual(@as(i32, 2), queue.dequeue());
    try std.testing.expectEqual(@as(i32, 3), queue.dequeue());
    try std.testing.expect(queue.isEmpty());
    try std.testing.expectEqual(@as(?i32, null), queue.dequeue());
}

test "Queue - ring buffer wraparound" {
    const allocator = std.testing.allocator;
    var queue = try Queue(i32).initWithCapacity(allocator, 4);
    defer queue.deinit();

    // Fill and partially drain to test wraparound
    try queue.enqueue(1);
    try queue.enqueue(2);
    try queue.enqueue(3);
    try queue.enqueue(4);

    try std.testing.expectEqual(@as(i32, 1), queue.dequeue());
    try std.testing.expectEqual(@as(i32, 2), queue.dequeue());

    // Now head is at position 2, add more items
    try queue.enqueue(5);
    try queue.enqueue(6);

    try std.testing.expectEqual(@as(usize, 4), queue.len());
    try std.testing.expectEqual(@as(i32, 3), queue.dequeue());
    try std.testing.expectEqual(@as(i32, 4), queue.dequeue());
    try std.testing.expectEqual(@as(i32, 5), queue.dequeue());
    try std.testing.expectEqual(@as(i32, 6), queue.dequeue());
}

test "LinkedList - basic operations" {
    const allocator = std.testing.allocator;
    var list = LinkedList(i32).init(allocator);
    defer list.deinit();

    try std.testing.expect(list.isEmpty());

    try list.pushBack(2);
    try list.pushFront(1);
    try list.pushBack(3);

    try std.testing.expectEqual(@as(usize, 3), list.len());
    try std.testing.expectEqual(@as(i32, 1), list.peekFront());
    try std.testing.expectEqual(@as(i32, 3), list.peekBack());

    try std.testing.expectEqual(@as(i32, 1), list.popFront());
    try std.testing.expectEqual(@as(i32, 3), list.popBack());
    try std.testing.expectEqual(@as(i32, 2), list.popFront());

    try std.testing.expect(list.isEmpty());
}

test "LinkedList - iteration" {
    const allocator = std.testing.allocator;
    var list = LinkedList(i32).init(allocator);
    defer list.deinit();

    try list.pushBack(1);
    try list.pushBack(2);
    try list.pushBack(3);

    var iter = list.iterator();
    try std.testing.expectEqual(@as(i32, 1), iter.next());
    try std.testing.expectEqual(@as(i32, 2), iter.next());
    try std.testing.expectEqual(@as(i32, 3), iter.next());
    try std.testing.expectEqual(@as(?i32, null), iter.next());
}

test "LinkedList - indexOf and remove" {
    const allocator = std.testing.allocator;
    var list = LinkedList(i32).init(allocator);
    defer list.deinit();

    try list.pushBack(1);
    try list.pushBack(2);
    try list.pushBack(3);

    try std.testing.expectEqual(@as(?usize, 0), list.indexOf(1));
    try std.testing.expectEqual(@as(?usize, 1), list.indexOf(2));
    try std.testing.expectEqual(@as(?usize, 2), list.indexOf(3));
    try std.testing.expectEqual(@as(?usize, null), list.indexOf(99));

    try std.testing.expect(list.remove(2));
    try std.testing.expectEqual(@as(usize, 2), list.len());
    try std.testing.expectEqual(@as(?usize, null), list.indexOf(2));
    try std.testing.expect(!list.remove(99));
}

test "Deque - basic operations" {
    const allocator = std.testing.allocator;
    var deque = Deque(i32).init(allocator);
    defer deque.deinit();

    try std.testing.expect(deque.isEmpty());

    try deque.pushBack(2);
    try deque.pushFront(1);
    try deque.pushBack(3);

    try std.testing.expectEqual(@as(usize, 3), deque.len());
    try std.testing.expectEqual(@as(i32, 1), deque.peekFront());
    try std.testing.expectEqual(@as(i32, 3), deque.peekBack());

    try std.testing.expectEqual(@as(i32, 1), deque.popFront());
    try std.testing.expectEqual(@as(i32, 3), deque.popBack());
    try std.testing.expectEqual(@as(i32, 2), deque.popFront());

    try std.testing.expect(deque.isEmpty());
}

test "Deque - random access" {
    const allocator = std.testing.allocator;
    var deque = Deque(i32).init(allocator);
    defer deque.deinit();

    for (0..10) |i| {
        try deque.pushBack(@intCast(i));
    }

    for (0..10) |i| {
        try std.testing.expectEqual(@as(i32, @intCast(i)), deque.get(i));
    }
    try std.testing.expectEqual(@as(?i32, null), deque.get(10));
}

test "PriorityQueue - max heap" {
    const allocator = std.testing.allocator;
    var pq = PriorityQueue(i32, false).init(allocator); // max heap
    defer pq.deinit();

    try pq.insert(3);
    try pq.insert(1);
    try pq.insert(4);
    try pq.insert(1);
    try pq.insert(5);

    try std.testing.expectEqual(@as(usize, 5), pq.len());
    try std.testing.expectEqual(@as(i32, 5), pq.peek());

    try std.testing.expectEqual(@as(i32, 5), pq.pop());
    try std.testing.expectEqual(@as(i32, 4), pq.pop());
    try std.testing.expectEqual(@as(i32, 3), pq.pop());
    try std.testing.expectEqual(@as(i32, 1), pq.pop());
    try std.testing.expectEqual(@as(i32, 1), pq.pop());

    try std.testing.expect(pq.isEmpty());
    try std.testing.expectEqual(@as(?i32, null), pq.pop());
}

test "PriorityQueue - min heap" {
    const allocator = std.testing.allocator;
    var pq = PriorityQueue(i32, true).init(allocator); // min heap
    defer pq.deinit();

    try pq.insert(5);
    try pq.insert(3);
    try pq.insert(1);
    try pq.insert(4);
    try pq.insert(2);

    try std.testing.expectEqual(@as(i32, 1), pq.pop());
    try std.testing.expectEqual(@as(i32, 2), pq.pop());
    try std.testing.expectEqual(@as(i32, 3), pq.pop());
    try std.testing.expectEqual(@as(i32, 4), pq.pop());
    try std.testing.expectEqual(@as(i32, 5), pq.pop());
}

test "HashSet - basic operations" {
    const allocator = std.testing.allocator;
    var set = HashSet(i32).init(allocator);
    defer set.deinit();

    try std.testing.expect(set.isEmpty());

    try std.testing.expect(try set.insert(1));
    try std.testing.expect(!try set.insert(1)); // Already exists
    try std.testing.expect(try set.insert(2));
    try std.testing.expect(try set.insert(3));

    try std.testing.expectEqual(@as(usize, 3), set.len());
    try std.testing.expect(set.contains(1));
    try std.testing.expect(set.contains(2));
    try std.testing.expect(set.contains(3));
    try std.testing.expect(!set.contains(4));

    try std.testing.expect(set.remove(2));
    try std.testing.expect(!set.contains(2));
    try std.testing.expect(!set.remove(99)); // Doesn't exist
}

test "HashSet - iteration" {
    const allocator = std.testing.allocator;
    var set = HashSet(i32).init(allocator);
    defer set.deinit();

    _ = try set.insert(1);
    _ = try set.insert(2);
    _ = try set.insert(3);

    var count: usize = 0;
    var sum: i32 = 0;
    var iter = set.iterator();
    while (iter.next()) |item| {
        count += 1;
        sum += item;
    }

    try std.testing.expectEqual(@as(usize, 3), count);
    try std.testing.expectEqual(@as(i32, 6), sum);
}

test "Stack - large number of items" {
    const allocator = std.testing.allocator;
    var stack = Stack(i32).init(allocator);
    defer stack.deinit();

    // Push 1000 items
    for (0..1000) |i| {
        try stack.push(@intCast(i));
    }

    try std.testing.expectEqual(@as(usize, 1000), stack.len());

    // Pop all items (should be in reverse order)
    var expected: i32 = 999;
    while (stack.pop()) |item| {
        try std.testing.expectEqual(expected, item);
        expected -= 1;
    }

    try std.testing.expectEqual(@as(i32, -1), expected);
}

test "Queue - large number of items" {
    const allocator = std.testing.allocator;
    var queue = Queue(i32).init(allocator);
    defer queue.deinit();

    // Enqueue 1000 items
    for (0..1000) |i| {
        try queue.enqueue(@intCast(i));
    }

    try std.testing.expectEqual(@as(usize, 1000), queue.len());

    // Dequeue all items (should be in same order)
    var expected: i32 = 0;
    while (queue.dequeue()) |item| {
        try std.testing.expectEqual(expected, item);
        expected += 1;
    }

    try std.testing.expectEqual(@as(i32, 1000), expected);
}

test "LinkedList - large number of items" {
    const allocator = std.testing.allocator;
    var list = LinkedList(i32).init(allocator);
    defer list.deinit();

    // Push 1000 items
    for (0..1000) |i| {
        try list.pushBack(@intCast(i));
    }

    try std.testing.expectEqual(@as(usize, 1000), list.len());

    // Pop from front (should be in order)
    var expected: i32 = 0;
    while (list.popFront()) |item| {
        try std.testing.expectEqual(expected, item);
        expected += 1;
    }

    try std.testing.expectEqual(@as(i32, 1000), expected);
}

test "Deque - large number of items" {
    const allocator = std.testing.allocator;
    var deque = Deque(i32).init(allocator);
    defer deque.deinit();

    // Push 1000 items alternating front and back
    for (0..1000) |i| {
        if (i % 2 == 0) {
            try deque.pushBack(@intCast(i));
        } else {
            try deque.pushFront(@intCast(i));
        }
    }

    try std.testing.expectEqual(@as(usize, 1000), deque.len());

    // Clear and verify
    deque.clear();
    try std.testing.expect(deque.isEmpty());
}

test "PriorityQueue - large number of items" {
    const allocator = std.testing.allocator;
    var pq = PriorityQueue(i32, true).init(allocator); // min heap
    defer pq.deinit();

    // Insert 1000 items in random-ish order
    var i: i32 = 0;
    while (i < 1000) : (i += 1) {
        try pq.insert(@rem(i * 7919, 1000)); // Simple pseudo-random
    }

    // Should come out sorted
    var prev: i32 = -1;
    while (pq.pop()) |item| {
        try std.testing.expect(item >= prev);
        prev = item;
    }
}