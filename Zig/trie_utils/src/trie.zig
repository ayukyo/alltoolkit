const std = @import("std");
const Allocator = std.mem.Allocator;

/// Trie (Prefix Tree) implementation for efficient string storage and prefix operations
/// Supports insert, search, delete, autocomplete, and pattern matching
pub fn Trie(comptime max_word_size: usize) type {
    return struct {
        const Self = @This();

        /// Node in the Trie
        const Node = struct {
            children: [26]?*Node,
            is_end: bool,
            word_count: usize, // Number of complete words in this subtree
            child_count: usize, // Number of child nodes

            fn init(allocator: Allocator) Allocator.Error!*Node {
                const node = try allocator.create(Node);
                @memset(&node.children, null);
                node.is_end = false;
                node.word_count = 0;
                node.child_count = 0;
                return node;
            }

            fn deinit(self: *Node, allocator: Allocator) void {
                for (&self.children) |child_opt| {
                    if (child_opt) |child| {
                        child.deinit(allocator);
                    }
                }
                allocator.destroy(self);
            }
        };

        root: *Node,
        allocator: Allocator,
        size: usize, // Total number of words

        /// Initialize a new Trie
        pub fn init(allocator: Allocator) Allocator.Error!Self {
            const root = try Node.init(allocator);
            return .{
                .root = root,
                .allocator = allocator,
                .size = 0,
            };
        }

        /// Free all allocated memory
        pub fn deinit(self: *Self) void {
            self.root.deinit(self.allocator);
            self.* = undefined;
        }

        /// Get the number of words in the trie
        pub fn count(self: Self) usize {
            return self.size;
        }

        /// Check if the trie is empty
        pub fn isEmpty(self: Self) bool {
            return self.size == 0;
        }

        /// Convert a character to an index (0-25)
        fn charToIndex(c: u8) ?usize {
            if (c >= 'a' and c <= 'z') {
                return @as(usize, c - 'a');
            } else if (c >= 'A' and c <= 'Z') {
                return @as(usize, c - 'A');
            }
            return null;
        }

        /// Convert an index back to a character
        fn indexToChar(index: usize) u8 {
            return @as(u8, @intCast(index + @as(usize, 'a')));
        }

        /// Insert a word into the trie
        /// Returns true if the word was newly inserted, false if it already existed or is invalid
        pub fn insert(self: *Self, word: []const u8) Allocator.Error!bool {
            if (word.len == 0 or word.len > max_word_size) return false;

            var current = self.root;
            var path_nodes: [max_word_size]*Node = undefined;
            var path_len: usize = 0;

            for (word) |c| {
                const idx = charToIndex(c) orelse return false;
                if (current.children[idx] == null) {
                    current.children[idx] = try Node.init(self.allocator);
                    current.child_count += 1;
                }
                path_nodes[path_len] = current;
                path_len += 1;
                current = current.children[idx].?;
            }

            if (current.is_end) {
                return false; // Word already exists
            }

            current.is_end = true;
            self.size += 1;

            // Update word_count along the path (including the final node)
            for (0..path_len) |i| {
                path_nodes[i].word_count += 1;
            }
            current.word_count += 1; // Also increment the final node

            return true;
        }

        /// Insert multiple words into the trie
        /// Returns the number of words actually inserted
        pub fn insertBatch(self: *Self, words: []const []const u8) Allocator.Error!usize {
            var inserted: usize = 0;
            for (words) |word| {
                if (try self.insert(word)) {
                    inserted += 1;
                }
            }
            return inserted;
        }

        /// Search for a word in the trie
        pub fn search(self: Self, word: []const u8) bool {
            if (word.len == 0) return false;

            var current = self.root;
            for (word) |c| {
                const idx = charToIndex(c) orelse return false;
                current = current.children[idx] orelse return false;
            }
            return current.is_end;
        }

        /// Check if any word starts with the given prefix
        pub fn startsWith(self: Self, prefix: []const u8) bool {
            if (prefix.len == 0) return self.size > 0;

            var current = self.root;
            for (prefix) |c| {
                const idx = charToIndex(c) orelse return false;
                current = current.children[idx] orelse return false;
            }
            return true;
        }

        /// Count words with a given prefix
        pub fn countPrefix(self: Self, prefix: []const u8) usize {
            if (prefix.len == 0) return self.size;

            var current = self.root;
            for (prefix) |c| {
                const idx = charToIndex(c) orelse return 0;
                current = current.children[idx] orelse return 0;
            }
            return current.word_count;
        }

        /// Get the node at the end of a prefix, or null if not found
        fn getNode(self: Self, prefix: []const u8) ?*Node {
            if (prefix.len == 0) return self.root;

            var current = self.root;
            for (prefix) |c| {
                const idx = charToIndex(c) orelse return null;
                current = current.children[idx] orelse return null;
            }
            return current;
        }

        /// Collect all words with a given prefix
        pub fn getWordsWithPrefix(self: Self, allocator: Allocator, prefix: []const u8, max_results: usize) Allocator.Error![][]u8 {
            const start_node = self.getNode(prefix) orelse return &[_][]u8{};

            var result = std.ArrayList([]u8).init(allocator);
            defer result.deinit();

            var buffer: [max_word_size]u8 = undefined;
            @memcpy(buffer[0..prefix.len], prefix);

            try self.collectWords(allocator, start_node, &buffer, prefix.len, &result, max_results);
            return result.toOwnedSlice();
        }

        /// Collect all words starting from a node
        fn collectWords(
            self: Self,
            allocator: Allocator,
            node: *Node,
            buffer: *[max_word_size]u8,
            depth: usize,
            result: *std.ArrayList([]u8),
            max_results: usize,
        ) Allocator.Error!void {
            if (result.items.len >= max_results) return;

            if (node.is_end) {
                const word = try allocator.dupe(u8, buffer[0..depth]);
                try result.append(word);
            }

            if (result.items.len >= max_results) return;

            for (0..26) |i| {
                if (node.children[i]) |child| {
                    buffer[depth] = indexToChar(i);
                    try self.collectWords(allocator, child, buffer, depth + 1, result, max_results);
                    if (result.items.len >= max_results) return;
                }
            }
        }

        /// Get all words in the trie
        pub fn getAllWords(self: Self, allocator: Allocator) Allocator.Error![][]u8 {
            return self.getWordsWithPrefix(allocator, "", self.size);
        }

        /// Delete a word from the trie
        /// Returns true if the word was found and deleted, false otherwise
        pub fn delete(self: *Self, word: []const u8) bool {
            if (word.len == 0) return false;
            const existed = self.search(word);
            if (!existed) return false; // Word doesn't exist
            self.deleteHelper(self.root, word, 0);
            return true;
        }

        /// Helper function for deletion - updates internal state
        fn deleteHelper(self: *Self, node: *Node, word: []const u8, depth: usize) void {
            if (depth == word.len) {
                node.is_end = false;
                self.size -= 1;
                node.word_count = if (node.word_count > 0) node.word_count - 1 else 0;
                return;
            }

            const c = word[depth];
            const idx = charToIndex(c) orelse return;
            const child = node.children[idx] orelse return;

            self.deleteHelper(child, word, depth + 1);

            // Update word_count for this node
            node.word_count = if (node.word_count > 0) node.word_count - 1 else 0;

            // Check if child should be deleted
            if (!child.is_end and child.child_count == 0) {
                child.deinit(self.allocator);
                node.children[idx] = null;
                node.child_count -= 1;
            }
        }

        /// Find the longest common prefix among all words
        /// Writes the prefix to the output buffer and returns the length
        pub fn longestCommonPrefix(self: Self, output: []u8) usize {
            if (self.size == 0) return 0;

            var len: usize = 0;
            var current = self.root;

            while (len < output.len) {
                // If this is an end node, stop
                if (current.is_end) break;

                // Find the single child
                var single_child_idx: ?usize = null;
                var child_count: usize = 0;

                for (0..26) |i| {
                    if (current.children[i] != null) {
                        child_count += 1;
                        single_child_idx = i;
                    }
                }

                if (child_count != 1) break;

                const idx = single_child_idx.?;
                output[len] = indexToChar(idx);
                len += 1;
                current = current.children[idx].?;
            }

            return len;
        }

        /// Pattern matching with wildcards
        /// '?' matches any single character
        /// '*' matches zero or more characters
        pub fn patternMatch(self: Self, allocator: Allocator, pattern: []const u8, max_results: usize) Allocator.Error![][]u8 {
            var result = std.ArrayList([]u8).init(allocator);
            defer result.deinit();

            var buffer: [max_word_size]u8 = undefined;
            try self.patternMatchHelper(self.root, pattern, 0, &buffer, 0, &result, max_results);

            return result.toOwnedSlice();
        }

        fn patternMatchHelper(
            self: Self,
            node: *Node,
            pattern: []const u8,
            pattern_idx: usize,
            buffer: *[max_word_size]u8,
            depth: usize,
            result: *std.ArrayList([]u8),
            max_results: usize,
        ) Allocator.Error!void {
            if (result.items.len >= max_results) return;

            // Handle wildcard '*'
            if (pattern_idx < pattern.len and pattern[pattern_idx] == '*') {
                // Zero or more characters
                // Try matching zero characters first
                try self.patternMatchHelper(node, pattern, pattern_idx + 1, buffer, depth, result, max_results);

                // Try matching one or more characters
                for (0..26) |i| {
                    if (node.children[i]) |child| {
                        buffer[depth] = indexToChar(i);
                        try self.patternMatchHelper(child, pattern, pattern_idx, buffer, depth + 1, result, max_results);
                    }
                }
                return;
            }

            // End of pattern
            if (pattern_idx == pattern.len) {
                if (node.is_end) {
                    const word = try self.allocator.dupe(u8, buffer[0..depth]);
                    try result.append(word);
                }
                return;
            }

            // Handle wildcard '?'
            if (pattern[pattern_idx] == '?') {
                for (0..26) |i| {
                    if (node.children[i]) |child| {
                        buffer[depth] = indexToChar(i);
                        try self.patternMatchHelper(child, pattern, pattern_idx + 1, buffer, depth + 1, result, max_results);
                    }
                }
                return;
            }

            // Exact character match
            const idx = charToIndex(pattern[pattern_idx]) orelse return;
            const child = node.children[idx] orelse return;
            buffer[depth] = pattern[pattern_idx];
            try self.patternMatchHelper(child, pattern, pattern_idx + 1, buffer, depth + 1, result, max_results);
        }

        /// Count total number of nodes in the trie
        pub fn nodeCount(self: Self) usize {
            return self.countNodes(self.root);
        }

        fn countNodes(self: Self, node: *Node) usize {
            var node_count: usize = 1;
            for (0..26) |i| {
                if (node.children[i]) |child| {
                    node_count += self.countNodes(child);
                }
            }
            return node_count;
        }

        /// Estimate memory usage in bytes
        pub fn memoryUsage(self: Self) usize {
            const nodes = self.nodeCount();
            // Each node: 26 pointers (208 bytes on 64-bit) + 2 bools/size_t
            return nodes * @sizeOf(Node);
        }

        /// Clear all words from the trie
        pub fn clear(self: *Self) Allocator.Error!void {
            // Deallocate all children of root
            for (0..26) |i| {
                if (self.root.children[i]) |child| {
                    child.deinit(self.allocator);
                    self.root.children[i] = null;
                }
            }
            self.root.child_count = 0;
            self.root.word_count = 0;
            self.root.is_end = false;
            self.size = 0;
        }
    };
}

// Tests
const testing = std.testing;
const TrieType = Trie(256);

test "Trie - basic insert and search" {
    const allocator = testing.allocator;
    var trie = try TrieType.init(allocator);
    defer trie.deinit();

    try testing.expect(try trie.insert("hello"));
    try testing.expect(try trie.insert("world"));
    try testing.expect(try trie.insert("hi"));

    try testing.expect(trie.search("hello"));
    try testing.expect(trie.search("world"));
    try testing.expect(trie.search("hi"));
    try testing.expect(!trie.search("hell"));
    try testing.expect(!trie.search("helloworld"));
}

test "Trie - duplicate insert" {
    const allocator = testing.allocator;
    var trie = try TrieType.init(allocator);
    defer trie.deinit();

    try testing.expect(try trie.insert("test"));
    try testing.expect(!try trie.insert("test")); // Second insert returns false
    try testing.expect(trie.count() == 1);
}

test "Trie - prefix operations" {
    const allocator = testing.allocator;
    var trie = try TrieType.init(allocator);
    defer trie.deinit();

    _ = try trie.insert("apple");
    _ = try trie.insert("app");
    _ = try trie.insert("application");
    _ = try trie.insert("apply");

    try testing.expect(trie.startsWith("app"));
    try testing.expect(trie.startsWith("appl"));
    try testing.expect(!trie.startsWith("banana"));

    try testing.expect(trie.countPrefix("app") == 4);
    try testing.expect(trie.countPrefix("appl") == 3);
    try testing.expect(trie.countPrefix("apple") == 1);
    try testing.expect(trie.countPrefix("applex") == 0);
}

test "Trie - autocomplete" {
    const allocator = testing.allocator;
    var trie = try TrieType.init(allocator);
    defer trie.deinit();

    _ = try trie.insert("cat");
    _ = try trie.insert("car");
    _ = try trie.insert("card");
    _ = try trie.insert("care");
    _ = try trie.insert("careful");
    _ = try trie.insert("dog");

    const words = try trie.getWordsWithPrefix(allocator, "car", 10);
    defer {
        for (words) |w| allocator.free(w);
        allocator.free(words);
    }

    try testing.expect(words.len == 4);

    // Check that all words start with "car"
    for (words) |word| {
        try testing.expect(std.mem.startsWith(u8, word, "car"));
    }
}

test "Trie - delete" {
    const allocator = testing.allocator;
    var trie = try TrieType.init(allocator);
    defer trie.deinit();

    _ = try trie.insert("hello");
    _ = try trie.insert("hell");
    _ = try trie.insert("help");

    try testing.expect(trie.search("hello"));
    try testing.expect(trie.delete("hello"));
    try testing.expect(!trie.search("hello"));
    try testing.expect(trie.search("hell"));
    try testing.expect(trie.search("help"));
    try testing.expect(!trie.delete("hello")); // Already deleted
}

test "Trie - longest common prefix" {
    const allocator = testing.allocator;
    var trie = try TrieType.init(allocator);
    defer trie.deinit();

    _ = try trie.insert("flower");
    _ = try trie.insert("flow");
    _ = try trie.insert("flight");

    var buf: [256]u8 = undefined;
    const lcp_len = trie.longestCommonPrefix(&buf);
    try testing.expectEqualSlices(u8, "fl", buf[0..lcp_len]);
}

test "Trie - pattern match with ?" {
    const allocator = testing.allocator;
    var trie = try TrieType.init(allocator);
    defer trie.deinit();

    _ = try trie.insert("cat");
    _ = try trie.insert("car");
    _ = try trie.insert("card");
    _ = try trie.insert("care");
    _ = try trie.insert("bat");
    _ = try trie.insert("bar");

    const matches = try trie.patternMatch(allocator, "ca?", 10);
    defer {
        for (matches) |m| allocator.free(m);
        allocator.free(matches);
    }

    try testing.expect(matches.len == 2); // cat, car
}

test "Trie - pattern match with *" {
    const allocator = testing.allocator;
    var trie = try TrieType.init(allocator);
    defer trie.deinit();

    _ = try trie.insert("cat");
    _ = try trie.insert("car");
    _ = try trie.insert("card");

    const matches = try trie.patternMatch(allocator, "ca*", 10);
    defer {
        for (matches) |m| allocator.free(m);
        allocator.free(matches);
    }

    try testing.expect(matches.len == 3);
}

test "Trie - batch insert" {
    const allocator = testing.allocator;
    var trie = try TrieType.init(allocator);
    defer trie.deinit();

    const words = [_][]const u8{ "one", "two", "three", "four", "five" };
    const inserted = try trie.insertBatch(&words);

    try testing.expectEqual(@as(usize, 5), inserted);
    try testing.expectEqual(@as(usize, 5), trie.count());
}

test "Trie - empty trie" {
    const allocator = testing.allocator;
    var trie = try TrieType.init(allocator);
    defer trie.deinit();

    try testing.expect(trie.isEmpty());
    try testing.expectEqual(@as(usize, 0), trie.count());
    try testing.expect(!trie.search("anything"));
    try testing.expect(!trie.startsWith("any"));
}

test "Trie - clear" {
    const allocator = testing.allocator;
    var trie = try TrieType.init(allocator);
    defer trie.deinit();

    _ = try trie.insert("one");
    _ = try trie.insert("two");
    _ = try trie.insert("three");

    try testing.expectEqual(@as(usize, 3), trie.count());

    try trie.clear();

    try testing.expect(trie.isEmpty());
    try testing.expectEqual(@as(usize, 0), trie.count());
}

test "Trie - node count and memory usage" {
    const allocator = testing.allocator;
    var trie = try TrieType.init(allocator);
    defer trie.deinit();

    _ = try trie.insert("a");
    _ = try trie.insert("ab");
    _ = try trie.insert("abc");

    const nodes = trie.nodeCount();
    try testing.expect(nodes >= 3); // At least 3 nodes

    const mem = trie.memoryUsage();
    try testing.expect(mem > 0);
}

test "Trie - case insensitive" {
    const allocator = testing.allocator;
    var trie = try TrieType.init(allocator);
    defer trie.deinit();

    _ = try trie.insert("Hello");
    _ = try trie.insert("WORLD");

    try testing.expect(trie.search("hello"));
    try testing.expect(trie.search("HELLO"));
    try testing.expect(trie.search("world"));
    try testing.expect(trie.search("World"));
}

test "Trie - single character words" {
    const allocator = testing.allocator;
    var trie = try TrieType.init(allocator);
    defer trie.deinit();

    _ = try trie.insert("a");
    _ = try trie.insert("b");
    _ = try trie.insert("c");

    try testing.expect(trie.search("a"));
    try testing.expect(trie.search("b"));
    try testing.expect(trie.search("c"));
    try testing.expectEqual(@as(usize, 3), trie.count());
}

test "Trie - get all words" {
    const allocator = testing.allocator;
    var trie = try TrieType.init(allocator);
    defer trie.deinit();

    const test_words = [_][]const u8{ "apple", "banana", "cherry", "date" };
    for (test_words) |word| {
        _ = try trie.insert(word);
    }

    const all_words = try trie.getAllWords(allocator);
    defer {
        for (all_words) |w| allocator.free(w);
        allocator.free(all_words);
    }

    try testing.expectEqual(@as(usize, 4), all_words.len);
}