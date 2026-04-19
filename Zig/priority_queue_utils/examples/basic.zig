const std = @import("std");
const PriorityQueue = @import("priority_queue").PriorityQueue;
const minCompare = @import("priority_queue").minCompare;
const maxCompare = @import("priority_queue").maxCompare;

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    
    const stdout = std.io.getStdOut().writer();
    
    try stdout.print("=== Priority Queue Basic Examples ===\n\n", .{});
    
    // Example 1: Min-Heap with integers
    try stdout.print("1. Min-Heap (smallest first):\n", .{});
    {
        var pq = PriorityQueue(i32).init(allocator, minCompare(i32));
        defer pq.deinit();
        
        try pq.insert(42);
        try pq.insert(10);
        try pq.insert(7);
        try pq.insert(99);
        try pq.insert(3);
        
        try stdout.print("   Inserted: 42, 10, 7, 99, 3\n", .{});
        try stdout.print("   Removing in priority order: ", .{});
        
        while (!pq.isEmpty()) {
            const item = pq.remove().?;
            try stdout.print("{} ", .{item});
        }
        try stdout.print("\n\n", .{});
    }
    
    // Example 2: Max-Heap with integers
    try stdout.print("2. Max-Heap (largest first):\n", .{});
    {
        var pq = PriorityQueue(i32).init(allocator, maxCompare(i32));
        defer pq.deinit();
        
        try pq.insert(42);
        try pq.insert(10);
        try pq.insert(7);
        try pq.insert(99);
        try pq.insert(3);
        
        try stdout.print("   Inserted: 42, 10, 7, 99, 3\n", .{});
        try stdout.print("   Removing in priority order: ", .{});
        
        while (!pq.isEmpty()) {
            const item = pq.remove().?;
            try stdout.print("{} ", .{item});
        }
        try stdout.print("\n\n", .{});
    }
    
    // Example 3: Peek without removing
    try stdout.print("3. Peek operation (view without removing):\n", .{});
    {
        var pq = PriorityQueue(i32).init(allocator, minCompare(i32));
        defer pq.deinit();
        
        try pq.insert(5);
        try pq.insert(1);
        try pq.insert(10);
        
        try stdout.print("   Top element: {}\n", .{pq.peek().?});
        try stdout.print("   Size: {}\n", .{pq.count()});
        try stdout.print("   Top element again: {}\n\n", .{pq.peek().?});
    }
    
    // Example 4: Dynamic growth
    try stdout.print("4. Dynamic growth (inserting many elements):\n", .{});
    {
        var pq = PriorityQueue(i32).init(allocator, minCompare(i32));
        defer pq.deinit();
        
        var i: i32 = 1000;
        while (i > 0) : (i -= 1) {
            try pq.insert(i);
        }
        
        try stdout.print("   Inserted 1000 elements\n", .{});
        try stdout.print("   First 10 items: ", .{});
        
        var count: usize = 0;
        while (count < 10 and !pq.isEmpty()) : (count += 1) {
            const item = pq.remove().?;
            try stdout.print("{} ", .{item});
        }
        try stdout.print("...\n\n", .{});
    }
    
    try stdout.print("=== All examples completed! ===\n", .{});
}