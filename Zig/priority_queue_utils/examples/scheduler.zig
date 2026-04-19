const std = @import("std");
const PriorityQueue = @import("priority_queue").PriorityQueue;

/// Task represents a scheduled task with priority
const Task = struct {
    priority: u32,
    id: u32,
    name: []const u8,
    
    fn compare(a: Task, b: Task) std.math.Order {
        return std.math.order(a.priority, b.priority);
    }
};

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    const stdout = std.io.getStdOut().writer();
    
    try stdout.print("=== Task Scheduler Example ===\n\n", .{});
    
    // Create a priority queue for tasks
    var scheduler = PriorityQueue(Task).init(allocator, Task.compare);
    defer scheduler.deinit();
    
    // Add tasks with different priorities
    try stdout.print("Adding tasks to scheduler:\n", .{});
    
    const tasks = [_]Task{
        .{ .priority = 10, .id = 1, .name = "Send email notifications" },
        .{ .priority = 1, .id = 2, .name = "Process payment" },
        .{ .priority = 5, .id = 3, .name = "Generate daily report" },
        .{ .priority = 1, .id = 4, .name = "Handle user login" },
        .{ .priority = 8, .id = 5, .name = "Backup database" },
        .{ .priority = 3, .id = 6, .name = "Clean temp files" },
        .{ .priority = 1, .id = 7, .name = "Sync user data" },
    };
    
    for (tasks) |task| {
        try scheduler.insert(task);
        try stdout.print("  [{d:0>3}] Priority {}: {s}\n", .{ task.id, task.priority, task.name });
    }
    
    try stdout.print("\nProcessing tasks by priority:\n", .{});
    try stdout.print("(Lower priority number = higher urgency)\n\n", .{});
    
    // Process tasks in priority order
    while (!scheduler.isEmpty()) {
        const task = scheduler.remove().?;
        try stdout.print("  [{d:0>3}] Priority {}: {s}\n", .{ task.id, task.priority, task.name });
    }
    
    try stdout.print("\n=== Scheduler demo completed! ===\n", .{});
}