const std = @import("std");
const Allocator = std.mem.Allocator;

/// Disjoint Set Union (Union-Find) data structure
/// Implements efficient union and find operations with:
/// - Path compression in find()
/// - Union by rank optimization
/// - O(α(n)) amortized time complexity (inverse Ackermann function)
pub fn DisjointSet(comptime T: type) type {
    return struct {
        const Self = @This();

        /// Node structure for each element
        const Node = struct {
            parent: usize,
            rank: usize,
        };

        nodes: []Node,
        values: []T,
        count: usize,
        allocator: Allocator,

        /// Initialize a new DisjointSet with given elements
        pub fn init(allocator: Allocator, elements: []const T) Allocator.Error!Self {
            const nodes = try allocator.alloc(Node, elements.len);
            errdefer allocator.free(nodes);

            const values = try allocator.alloc(T, elements.len);
            errdefer allocator.free(values);

            @memcpy(values, elements);

            // Initialize each element as its own parent (separate set)
            for (nodes, 0..) |*node, i| {
                node.parent = i;
                node.rank = 0;
            }

            return .{
                .nodes = nodes,
                .values = values,
                .count = elements.len,
                .allocator = allocator,
            };
        }

        /// Initialize with a range of indices [0, num_elements)
        pub fn initRange(allocator: Allocator, num_elements: usize) Allocator.Error!Self {
            const nodes = try allocator.alloc(Node, num_elements);
            errdefer allocator.free(nodes);

            const values = try allocator.alloc(T, num_elements);
            errdefer allocator.free(values);

            // Initialize indices as values
            for (nodes, values, 0..) |*node, *value, i| {
                node.parent = i;
                node.rank = 0;
                value.* = @intCast(i);
            }

            return .{
                .nodes = nodes,
                .values = values,
                .count = num_elements,
                .allocator = allocator,
            };
        }

        /// Free all allocated memory
        pub fn deinit(self: *Self) void {
            self.allocator.free(self.nodes);
            self.allocator.free(self.values);
            self.* = undefined;
        }

        /// Find the root/representative of the set containing element at index
        /// Uses path compression for optimization
        pub fn find(self: *Self, index: usize) usize {
            std.debug.assert(index < self.count);

            // Path compression: make every node on the path point directly to root
            if (self.nodes[index].parent != index) {
                self.nodes[index].parent = self.find(self.nodes[index].parent);
            }
            return self.nodes[index].parent;
        }

        /// Find root without path compression (const version)
        pub fn findConst(self: Self, index: usize) usize {
            std.debug.assert(index < self.count);

            var current = index;
            while (self.nodes[current].parent != current) {
                current = self.nodes[current].parent;
            }
            return current;
        }

        /// Check if two elements are in the same set
        pub fn connected(self: *Self, a: usize, b: usize) bool {
            return self.find(a) == self.find(b);
        }

        /// Union two sets containing elements at indices a and b
        /// Returns true if a union was performed, false if already in same set
        pub fn unionSets(self: *Self, a: usize, b: usize) bool {
            const root_a = self.find(a);
            const root_b = self.find(b);

            if (root_a == root_b) {
                return false; // Already in same set
            }

            // Union by rank: attach smaller rank tree under root of higher rank tree
            if (self.nodes[root_a].rank < self.nodes[root_b].rank) {
                self.nodes[root_a].parent = root_b;
            } else if (self.nodes[root_a].rank > self.nodes[root_b].rank) {
                self.nodes[root_b].parent = root_a;
            } else {
                // Same rank: make one the root and increment its rank
                self.nodes[root_b].parent = root_a;
                self.nodes[root_a].rank += 1;
            }

            return true;
        }

        /// Get the value at an index
        pub fn getValue(self: Self, index: usize) T {
            std.debug.assert(index < self.count);
            return self.values[index];
        }

        /// Get the number of elements
        pub fn size(self: Self) usize {
            return self.count;
        }

        /// Count the number of distinct sets (connected components)
        pub fn countSets(self: *Self) usize {
            var set_count: usize = 0;
            for (0..self.count) |i| {
                if (self.find(i) == i) {
                    set_count += 1;
                }
            }
            return set_count;
        }

        /// Get all elements in the same set as the given element
        pub fn getSetMembers(self: *Self, allocator: Allocator, index: usize) Allocator.Error![]T {
            const root = self.find(index);
            var members = std.ArrayList(T).init(allocator);
            errdefer members.deinit();

            for (0..self.count) |i| {
                if (self.find(i) == root) {
                    try members.append(self.values[i]);
                }
            }

            return members.toOwnedSlice();
        }

        /// Get all sets as a list of lists
        pub fn getAllSets(self: *Self, allocator: Allocator) Allocator.Error![][]T {
            var sets_map = std.AutoHashMap(usize, std.ArrayList(T)).init(allocator);
            defer {
                var iter = sets_map.iterator();
                while (iter.next()) |entry| {
                    entry.value_ptr.deinit();
                }
                sets_map.deinit();
            }

            for (0..self.count) |i| {
                const root = self.find(i);
                const gop = try sets_map.getOrPut(root);
                if (!gop.found_existing) {
                    gop.value_ptr.* = std.ArrayList(T).init(allocator);
                }
                try gop.value_ptr.append(self.values[i]);
            }

            var result = std.ArrayList([]T).init(allocator);
            errdefer {
                for (result.items) |set| {
                    allocator.free(set);
                }
                result.deinit();
            }

            var iter = sets_map.iterator();
            while (iter.next()) |entry| {
                try result.append(try entry.value_ptr.toOwnedSlice());
            }

            return result.toOwnedSlice();
        }

        /// Get the size of the set containing the given element
        pub fn getSetSize(self: *Self, index: usize) usize {
            const root = self.find(index);
            var set_count: usize = 0;
            for (0..self.count) |i| {
                if (self.find(i) == root) {
                    set_count += 1;
                }
            }
            return set_count;
        }

        /// Reset all elements to individual sets
        pub fn reset(self: *Self) void {
            for (self.nodes, 0..) |*node, i| {
                node.parent = i;
                node.rank = 0;
            }
        }
    };
}

/// Simple DisjointSet for usize values (common use case)
pub const USizeDisjointSet = DisjointSet(usize);

// Tests
test "DisjointSet - basic union and find" {
    const allocator = std.testing.allocator;

    var ds = try DisjointSet(i32).init(allocator, &[_]i32{ 1, 2, 3, 4, 5 });
    defer ds.deinit();

    // Initially, each element is in its own set
    try std.testing.expectEqual(@as(usize, 5), ds.countSets());
    try std.testing.expect(ds.connected(0, 0));
    try std.testing.expect(!ds.connected(0, 1));

    // Union 0 and 1
    try std.testing.expect(ds.unionSets(0, 1));
    try std.testing.expect(ds.connected(0, 1));
    try std.testing.expectEqual(@as(usize, 4), ds.countSets());

    // Union 2 and 3
    try std.testing.expect(ds.unionSets(2, 3));
    try std.testing.expect(ds.connected(2, 3));
    try std.testing.expectEqual(@as(usize, 3), ds.countSets());

    // Union 0 and 2 (transitive)
    try std.testing.expect(ds.unionSets(1, 2));
    try std.testing.expect(ds.connected(0, 3));
    try std.testing.expectEqual(@as(usize, 2), ds.countSets());
}

test "DisjointSet - union already connected" {
    const allocator = std.testing.allocator;

    var ds = try DisjointSet(i32).init(allocator, &[_]i32{ 10, 20, 30 });
    defer ds.deinit();

    _ = ds.unionSets(0, 1);
    // Try to union again
    try std.testing.expect(!ds.unionSets(0, 1));
    try std.testing.expect(!ds.unionSets(1, 0));
}

test "DisjointSet - initRange" {
    const allocator = std.testing.allocator;

    var ds = try USizeDisjointSet.initRange(allocator, 10);
    defer ds.deinit();

    try std.testing.expectEqual(@as(usize, 10), ds.size());
    try std.testing.expectEqual(@as(usize, 10), ds.countSets());

    // Union even numbers
    _ = ds.unionSets(0, 2);
    _ = ds.unionSets(2, 4);
    _ = ds.unionSets(4, 6);
    _ = ds.unionSets(6, 8);

    try std.testing.expect(ds.connected(0, 8));
    try std.testing.expect(!ds.connected(0, 1));
    try std.testing.expectEqual(@as(usize, 6), ds.countSets());
}

test "DisjointSet - getSetMembers" {
    const allocator = std.testing.allocator;

    var ds = try DisjointSet(i32).init(allocator, &[_]i32{ 100, 200, 300, 400, 500 });
    defer ds.deinit();

    _ = ds.unionSets(0, 2);
    _ = ds.unionSets(1, 3);

    const set0 = try ds.getSetMembers(allocator, 0);
    defer allocator.free(set0);
    try std.testing.expectEqual(@as(usize, 2), set0.len);

    const set1 = try ds.getSetMembers(allocator, 1);
    defer allocator.free(set1);
    try std.testing.expectEqual(@as(usize, 2), set1.len);

    const set4 = try ds.getSetMembers(allocator, 4);
    defer allocator.free(set4);
    try std.testing.expectEqual(@as(usize, 1), set4.len);
}

test "DisjointSet - getSetSize" {
    const allocator = std.testing.allocator;

    var ds = try DisjointSet(i32).init(allocator, &[_]i32{ 1, 2, 3, 4, 5, 6 });
    defer ds.deinit();

    try std.testing.expectEqual(@as(usize, 1), ds.getSetSize(0));

    _ = ds.unionSets(0, 1);
    try std.testing.expectEqual(@as(usize, 2), ds.getSetSize(0));
    try std.testing.expectEqual(@as(usize, 2), ds.getSetSize(1));

    _ = ds.unionSets(2, 3);
    _ = ds.unionSets(0, 2);
    try std.testing.expectEqual(@as(usize, 4), ds.getSetSize(0));
}

test "DisjointSet - getAllSets" {
    const allocator = std.testing.allocator;

    var ds = try DisjointSet(i32).init(allocator, &[_]i32{ 1, 2, 3, 4, 5 });
    defer ds.deinit();

    _ = ds.unionSets(0, 1);
    _ = ds.unionSets(2, 3);

    const sets = try ds.getAllSets(allocator);
    defer {
        for (sets) |set| {
            allocator.free(set);
        }
        allocator.free(sets);
    }

    try std.testing.expectEqual(@as(usize, 3), sets.len);
}

test "DisjointSet - reset" {
    const allocator = std.testing.allocator;

    var ds = try DisjointSet(i32).init(allocator, &[_]i32{ 1, 2, 3, 4, 5 });
    defer ds.deinit();

    _ = ds.unionSets(0, 1);
    _ = ds.unionSets(2, 3);
    _ = ds.unionSets(0, 2);

    try std.testing.expectEqual(@as(usize, 2), ds.countSets());

    ds.reset();

    try std.testing.expectEqual(@as(usize, 5), ds.countSets());
    try std.testing.expect(!ds.connected(0, 1));
}

test "DisjointSet - path compression" {
    const allocator = std.testing.allocator;

    var ds = try USizeDisjointSet.initRange(allocator, 100);
    defer ds.deinit();

    // Create a long chain
    for (0..99) |i| {
        _ = ds.unionSets(i, i + 1);
    }

    // After find(0), all nodes should have shallow paths
    _ = ds.find(0);

    // Verify all are connected
    try std.testing.expect(ds.connected(0, 99));
}

test "DisjointSet - union by rank" {
    const allocator = std.testing.allocator;

    var ds = try USizeDisjointSet.initRange(allocator, 16);
    defer ds.deinit();

    // Build a balanced tree through union by rank
    _ = ds.unionSets(0, 1);
    _ = ds.unionSets(2, 3);
    _ = ds.unionSets(0, 2);
    _ = ds.unionSets(4, 5);
    _ = ds.unionSets(6, 7);
    _ = ds.unionSets(4, 6);
    _ = ds.unionSets(0, 4);

    // All should be connected
    try std.testing.expect(ds.connected(0, 7));
    try std.testing.expectEqual(@as(usize, 9), ds.countSets());
}

test "DisjointSet - getValue" {
    const allocator = std.testing.allocator;

    const values = [_]i32{ 10, 20, 30, 40, 50 };
    var ds = try DisjointSet(i32).init(allocator, &values);
    defer ds.deinit();

    try std.testing.expectEqual(@as(i32, 10), ds.getValue(0));
    try std.testing.expectEqual(@as(i32, 20), ds.getValue(1));
    try std.testing.expectEqual(@as(i32, 50), ds.getValue(4));
}

test "DisjointSet - single element" {
    const allocator = std.testing.allocator;

    var ds = try DisjointSet(i32).init(allocator, &[_]i32{42});
    defer ds.deinit();

    try std.testing.expectEqual(@as(usize, 1), ds.countSets());
    try std.testing.expect(ds.connected(0, 0));
    try std.testing.expect(!ds.unionSets(0, 0)); // Can't union with itself
}

test "DisjointSet - large set" {
    const allocator = std.testing.allocator;

    var ds = try USizeDisjointSet.initRange(allocator, 1000);
    defer ds.deinit();

    // Union in pairs
    var i: usize = 0;
    while (i < 1000) : (i += 2) {
        if (i + 1 < 1000) {
            _ = ds.unionSets(i, i + 1);
        }
    }

    try std.testing.expectEqual(@as(usize, 500), ds.countSets());
}

test "DisjointSet - findConst" {
    const allocator = std.testing.allocator;

    var ds = try USizeDisjointSet.initRange(allocator, 5);
    defer ds.deinit();

    _ = ds.unionSets(0, 1);
    _ = ds.unionSets(1, 2);

    // findConst should work without path compression
    const root = ds.findConst(2);
    try std.testing.expect(root < 3);
}