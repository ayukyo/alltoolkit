const std = @import("std");
const PriorityQueue = @import("priority_queue").PriorityQueue;

/// Graph node with distance for Dijkstra's algorithm
const Node = struct {
    distance: u32,
    vertex: usize,
    
    fn compare(a: Node, b: Node) std.math.Order {
        return std.math.order(a.distance, b.distance);
    }
};

/// Simple graph representation using adjacency list
const Graph = struct {
    allocator: std.mem.Allocator,
    adjacency: std.ArrayList(std.ArrayList(Edge)),
    
    const Edge = struct {
        to: usize,
        weight: u32,
    };
    
    fn init(allocator: std.mem.Allocator, vertex_count: usize) !Graph {
        var adjacency = try std.ArrayList(std.ArrayList(Edge)).initCapacity(allocator, vertex_count);
        errdefer adjacency.deinit();
        
        var i: usize = 0;
        while (i < vertex_count) : (i += 1) {
            try adjacency.append(std.ArrayList(Edge).init(allocator));
        }
        
        return .{
            .allocator = allocator,
            .adjacency = adjacency,
        };
    }
    
    fn deinit(self: *Graph) void {
        for (self.adjacency.items) |*list| {
            list.deinit();
        }
        self.adjacency.deinit();
    }
    
    fn addEdge(self: *Graph, from: usize, to: usize, weight: u32) !void {
        try self.adjacency.items[from].append(.{ .to = to, .weight = weight });
    }
    
    /// Dijkstra's shortest path algorithm
    fn dijkstra(self: Graph, start: usize, distances: []u32) void {
        // Initialize distances to infinity
        for (distances) |*d| {
            d.* = std.math.maxInt(u32);
        }
        distances[start] = 0;
        
        // Priority queue for vertices to visit
        var pq = PriorityQueue(Node).init(self.allocator, Node.compare);
        defer pq.deinit();
        
        pq.insert(.{ .distance = 0, .vertex = start }) catch return;
        
        while (!pq.isEmpty()) {
            const current = pq.remove().?;
            
            // Skip if we've already found a better path
            if (current.distance > distances[current.vertex]) {
                continue;
            }
            
            // Check all neighbors
            for (self.adjacency.items[current.vertex].items) |edge| {
                const new_dist = current.distance + edge.weight;
                if (new_dist < distances[edge.to]) {
                    distances[edge.to] = new_dist;
                    pq.insert(.{ .distance = new_dist, .vertex = edge.to }) catch {};
                }
            }
        }
    }
};

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    const stdout = std.io.getStdOut().writer();
    
    try stdout.print("=== Dijkstra's Shortest Path Algorithm ===\n\n", .{});
    
    // Create a sample graph:
    // 
    //     (0) --4-- (1) --1-- (2)
    //      |        |         |
    //      1        2         5
    //      |        |         |
    //     (3) --3-- (4) --1-- (5)
    //
    
    try stdout.print("Graph structure:\n", .{});
    try stdout.print("     (0) --4-- (1) --1-- (2)\n", .{});
    try stdout.print("      |        |         |\n", .{});
    try stdout.print("      1        2         5\n", .{});
    try stdout.print("      |        |         |\n", .{});
    try stdout.print("     (3) --3-- (4) --1-- (5)\n\n", .{});
    
    var graph = try Graph.init(allocator, 6);
    defer graph.deinit();
    
    // Add edges (undirected graph)
    try graph.addEdge(0, 1, 4);
    try graph.addEdge(1, 0, 4);
    try graph.addEdge(0, 3, 1);
    try graph.addEdge(3, 0, 1);
    try graph.addEdge(1, 2, 1);
    try graph.addEdge(2, 1, 1);
    try graph.addEdge(1, 4, 2);
    try graph.addEdge(4, 1, 2);
    try graph.addEdge(2, 5, 5);
    try graph.addEdge(5, 2, 5);
    try graph.addEdge(3, 4, 3);
    try graph.addEdge(4, 3, 3);
    try graph.addEdge(4, 5, 1);
    try graph.addEdge(5, 4, 1);
    
    // Run Dijkstra from vertex 0
    const distances = try allocator.alloc(u32, 6);
    defer allocator.free(distances);
    
    graph.dijkstra(0, distances);
    
    try stdout.print("Shortest distances from vertex 0:\n", .{});
    for (distances, 0..) |dist, i| {
        if (dist == std.math.maxInt(u32)) {
            try stdout.print("  Vertex {}: unreachable\n", .{i});
        } else {
            try stdout.print("  Vertex {}: {}\n", .{ i, dist });
        }
    }
    
    try stdout.print("\n=== Demo completed! ===\n", .{});
}