const std = @import("std");
const ds = @import("data-structures");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== Advanced Data Structures Examples ===\n\n", .{});

    // ========================================
    // Expression Evaluation using Stack
    // ========================================
    std.debug.print("--- Stack: Simple Calculator ---\n", .{});
    
    // Evaluate: ((3 + 4) * 2) = 14
    var calc_stack = ds.Stack(i32).init(allocator);
    defer calc_stack.deinit();

    // Push operands
    try calc_stack.push(3);
    try calc_stack.push(4);
    
    // Add
    const b = calc_stack.pop().?;
    const a = calc_stack.pop().?;
    try calc_stack.push(a + b);
    std.debug.print("After addition: {?} (stack has 7)\n", .{calc_stack.peek()});

    // Multiply
    try calc_stack.push(2);
    const m2 = calc_stack.pop().?;
    const m1 = calc_stack.pop().?;
    try calc_stack.push(m1 * m2);
    std.debug.print("Result: {?} (should be 14)\n\n", .{calc_stack.peek()});

    // ========================================
    // BFS using Queue
    // ========================================
    std.debug.print("--- Queue: Breadth-First Search ---\n", .{});
    
    // Simple BFS on a small tree-like structure
    // Tree: 1 -> [2, 3], 2 -> [4, 5], 3 -> [6, 7]
    const nodes = [_][]const u8{ "1", "2", "3", "4", "5", "6", "7" };
    const children = [_][]const usize{
        &[_]usize{1, 2}, // 1's children: 2, 3
        &[_]usize{3, 4}, // 2's children: 4, 5
        &[_]usize{5, 6}, // 3's children: 6, 7
        &[_]usize{},     // 4 has no children
        &[_]usize{},     // 5 has no children
        &[_]usize{},     // 6 has no children
        &[_]usize{},     // 7 has no children
    };

    var bfs_queue = ds.Queue(usize).init(allocator);
    defer bfs_queue.deinit();

    // Use a simple visited set with indices
    var visited = [7]bool{ false, false, false, false, false, false, false };

    try bfs_queue.enqueue(0); // Start from root (node 1 at index 0)
    visited[0] = true;

    std.debug.print("BFS traversal: ", .{});
    while (bfs_queue.dequeue()) |current| {
        std.debug.print("{s} ", .{nodes[current]});
        
        for (children[current]) |child| {
            if (!visited[child]) {
                visited[child] = true;
                try bfs_queue.enqueue(child);
            }
        }
    }
    std.debug.print("\nExpected: 1 2 3 4 5 6 7\n\n", .{});

    // ========================================
    // Task Scheduler using PriorityQueue
    // ========================================
    std.debug.print("--- PriorityQueue: Task Scheduler ---\n", .{});
    
    // Use i32 for priority (higher priority = more urgent, so max heap)
    var task_queue = ds.PriorityQueue(i32, false).init(allocator);
    defer task_queue.deinit();

    const tasks = [_]struct { priority: i32, name: []const u8 }{
        .{ .priority = 5, .name = "Critical bug fix" },
        .{ .priority = 3, .name = "Feature development" },
        .{ .priority = 1, .name = "Documentation" },
        .{ .priority = 4, .name = "Security patch" },
        .{ .priority = 2, .name = "Code review" },
    };

    for (tasks) |task| {
        try task_queue.insert(task.priority);
    }

    std.debug.print("Tasks in priority order:\n", .{});
    while (task_queue.pop()) |priority| {
        // Find matching task name
        for (tasks) |task| {
            if (task.priority == priority) {
                std.debug.print("  Priority {}: {s}\n", .{priority, task.name});
                break;
            }
        }
    }
    std.debug.print("\n", .{});

    // ========================================
    // Undo/Redo using Deque
    // ========================================
    std.debug.print("--- Deque: Undo/Redo System ---\n", .{});
    
    const Action = struct {
        id: i32,
        name: []const u8,
    };

    var history = ds.Deque(Action).init(allocator);
    defer history.deinit();

    // User performs actions
    try history.pushBack(.{ .id = 1, .name = "Draw line" });
    try history.pushBack(.{ .id = 2, .name = "Add circle" });
    try history.pushBack(.{ .id = 3, .name = "Apply color" });

    std.debug.print("Actions performed: ", .{});
    for (0..history.len()) |i| {
        if (history.get(i)) |action| {
            std.debug.print("{s} ", .{action.name});
        }
    }
    std.debug.print("\n", .{});

    // User undoes 2 actions (pop from back)
    std.debug.print("Undo: {s}\n", .{history.popBack().?.name});
    std.debug.print("Undo: {s}\n", .{history.popBack().?.name});
    std.debug.print("Current actions: {s}\n", .{history.get(0).?.name});

    // User performs new action (push to back)
    try history.pushBack(.{ .id = 4, .name = "Resize" });
    std.debug.print("New action: Resize\n", .{});
    std.debug.print("Current history size: {}\n\n", .{history.len()});

    // ========================================
    // Unique Counter using HashSet
    // ========================================
    std.debug.print("--- HashSet: Unique IDs Counter ---\n", .{});
    
    const ids = [_]i32{ 101, 102, 101, 103, 102, 104, 101 };
    var unique_ids = ds.HashSet(i32).init(allocator);
    defer unique_ids.deinit();

    var unique_count: usize = 0;
    for (ids) |id| {
        if (try unique_ids.insert(id)) {
            unique_count += 1;
        }
    }

    std.debug.print("Input IDs: 101, 102, 101, 103, 102, 104, 101\n", .{});
    std.debug.print("Unique IDs: {}\n", .{unique_count});
    std.debug.print("Unique set contains: ", .{});
    var id_iter = unique_ids.iterator();
    while (id_iter.next()) |id| {
        std.debug.print("{} ", .{id});
    }
    std.debug.print("\n\n", .{});

    // ========================================
    // Custom Types with LinkedList
    // ========================================
    std.debug.print("--- LinkedList: Custom Struct ---\n", .{});
    
    const Person = struct {
        id: i32,
        age: i32,
    };

    var people_list = ds.LinkedList(Person).init(allocator);
    defer people_list.deinit();

    try people_list.pushBack(.{ .id = 1, .age = 30 });
    try people_list.pushBack(.{ .id = 2, .age = 25 });
    try people_list.pushFront(.{ .id = 3, .age = 35 });

    std.debug.print("People (front to back):\n", .{});
    var people_iter = people_list.iterator();
    while (people_iter.next()) |person| {
        std.debug.print("  ID {}, Age {} ", .{person.id, person.age});
    }
    std.debug.print("\n", .{});

    // Find someone
    const bob_index = people_list.indexOf(.{ .id = 2, .age = 25 });
    std.debug.print("Person with ID 2, Age 25 is at index: {?}\n", .{bob_index});

    // Remove someone
    const removed = people_list.remove(.{ .id = 2, .age = 25 });
    std.debug.print("Removed person ID 2: {}\n", .{removed});
    std.debug.print("Remaining count: {}\n\n", .{people_list.len()});

    std.debug.print("=== Advanced Examples Complete ===\n", .{});
}