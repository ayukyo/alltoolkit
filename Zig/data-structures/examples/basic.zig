const std = @import("std");
const ds = @import("data-structures");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== Data Structures Library Demo ===\n\n", .{});

    // ========================================
    // Stack Demo
    // ========================================
    std.debug.print("--- Stack (LIFO) ---\n", .{});
    var stack = ds.Stack(i32).init(allocator);
    defer stack.deinit();

    try stack.push(10);
    try stack.push(20);
    try stack.push(30);
    
    std.debug.print("Pushed: 10, 20, 30\n", .{});
    std.debug.print("Size: {} items\n", .{stack.len()});
    std.debug.print("Top: {?} (peek)\n", .{stack.peek()});

    std.debug.print("Pop: {?}\n", .{stack.pop()});
    std.debug.print("Pop: {?}\n", .{stack.pop()});
    std.debug.print("Pop: {?}\n", .{stack.pop()});
    std.debug.print("Is empty: {}\n\n", .{stack.isEmpty()});

    // ========================================
    // Queue Demo
    // ========================================
    std.debug.print("--- Queue (FIFO) ---\n", .{});
    var queue = ds.Queue(i32).init(allocator);
    defer queue.deinit();

    try queue.enqueue(1);
    try queue.enqueue(2);
    try queue.enqueue(3);

    std.debug.print("Enqueued: 1, 2, 3\n", .{});
    std.debug.print("Size: {} items\n", .{queue.len()});
    std.debug.print("Front: {?} (peek)\n", .{queue.peek()});

    std.debug.print("Dequeue: {?}\n", .{queue.dequeue()});
    std.debug.print("Dequeue: {?}\n", .{queue.dequeue()});
    std.debug.print("Dequeue: {?}\n", .{queue.dequeue()});
    std.debug.print("Is empty: {}\n\n", .{queue.isEmpty()});

    // ========================================
    // LinkedList Demo
    // ========================================
    std.debug.print("--- LinkedList ---\n", .{});
    var list = ds.LinkedList(i32).init(allocator);
    defer list.deinit();

    try list.pushBack(2);
    try list.pushFront(1);
    try list.pushBack(3);

    std.debug.print("Added: 1 (front), 2 (back), 3 (back)\n", .{});
    std.debug.print("Size: {} items\n", .{list.len()});
    std.debug.print("Front: {?}, Back: {?}\n", .{list.peekFront(), list.peekBack()});

    std.debug.print("Iterating: ", .{});
    var iter = list.iterator();
    while (iter.next()) |item| {
        std.debug.print("{} ", .{item});
    }
    std.debug.print("\n\n", .{});

    // ========================================
    // Deque Demo
    // ========================================
    std.debug.print("--- Deque (Double-ended Queue) ---\n", .{});
    var deque = ds.Deque(i32).init(allocator);
    defer deque.deinit();

    try deque.pushFront(1);
    try deque.pushBack(3);
    try deque.pushFront(0);
    try deque.pushBack(4);

    std.debug.print("Added: 0, 1 (front), 3, 4 (back)\n", .{});
    std.debug.print("Size: {} items\n", .{deque.len()});
    std.debug.print("Front: {?}, Back: {?}\n", .{deque.peekFront(), deque.peekBack()});

    std.debug.print("Random access (index 1): {?}\n", .{deque.get(1)});
    std.debug.print("PopFront: {?}, PopBack: {?}\n\n", .{deque.popFront(), deque.popBack()});

    // ========================================
    // PriorityQueue Demo
    // ========================================
    std.debug.print("--- PriorityQueue (Min-Heap) ---\n", .{});
    var min_heap = ds.PriorityQueue(i32, true).init(allocator);
    defer min_heap.deinit();

    try min_heap.insert(50);
    try min_heap.insert(10);
    try min_heap.insert(30);
    try min_heap.insert(20);
    try min_heap.insert(40);

    std.debug.print("Inserted: 50, 10, 30, 20, 40\n", .{});
    std.debug.print("Size: {} items\n", .{min_heap.len()});
    std.debug.print("Top (min): {?}\n", .{min_heap.peek()});

    std.debug.print("Popping all (sorted order): ", .{});
    while (min_heap.pop()) |item| {
        std.debug.print("{} ", .{item});
    }
    std.debug.print("\n\n", .{});

    // ========================================
    // HashSet Demo
    // ========================================
    std.debug.print("--- HashSet ---\n", .{});
    var set = ds.HashSet(i32).init(allocator);
    defer set.deinit();

    _ = try set.insert(1);
    _ = try set.insert(2);
    _ = try set.insert(3);
    const already_exists = try set.insert(2);

    std.debug.print("Inserted: 1, 2, 3 (2 was already: {})\n", .{already_exists});
    std.debug.print("Size: {} items\n", .{set.len()});
    std.debug.print("Contains 2: {}, Contains 99: {}\n", .{set.contains(2), set.contains(99)});

    std.debug.print("Removed 2: {}\n", .{set.remove(2)});
    std.debug.print("Size after remove: {}\n", .{set.len()});

    std.debug.print("\n=== Demo Complete ===\n", .{});
}