const std = @import("std");
const Trie = @import("trie").Trie;

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== Trie Basic Usage Example ===\n\n", .{});

    // Create a trie
    var trie = try Trie(256).init(allocator);
    defer trie.deinit();

    // Insert words
    std.debug.print("Inserting words: apple, app, application, apply, banana, band, bandana\n", .{});
    _ = try trie.insert("apple");
    _ = try trie.insert("app");
    _ = try trie.insert("application");
    _ = try trie.insert("apply");
    _ = try trie.insert("banana");
    _ = try trie.insert("band");
    _ = try trie.insert("bandana");

    std.debug.print("Total words: {}\n\n", .{trie.count()});

    // Search operations
    std.debug.print("--- Search Operations ---\n", .{});
    std.debug.print("Search 'apple': {}\n", .{trie.search("apple")});
    std.debug.print("Search 'app': {}\n", .{trie.search("app")});
    std.debug.print("Search 'appl': {} (prefix only, not a complete word)\n", .{trie.search("appl")});
    std.debug.print("Search 'application': {}\n", .{trie.search("application")});
    std.debug.print("Search 'orange': {}\n", .{trie.search("orange")});
    std.debug.print("\n", .{});

    // Prefix operations
    std.debug.print("--- Prefix Operations ---\n", .{});
    std.debug.print("Starts with 'app': {}\n", .{trie.startsWith("app")});
    std.debug.print("Starts with 'ban': {}\n", .{trie.startsWith("ban")});
    std.debug.print("Starts with 'orange': {}\n", .{trie.startsWith("orange")});
    std.debug.print("Words with prefix 'app': {}\n", .{trie.countPrefix("app")});
    std.debug.print("Words with prefix 'ban': {}\n", .{trie.countPrefix("ban")});
    std.debug.print("Words with prefix 'band': {}\n", .{trie.countPrefix("band")});
    std.debug.print("\n", .{});

    // Autocomplete
    std.debug.print("--- Autocomplete ---\n", .{});
    const words = try trie.getWordsWithPrefix(allocator, "app", 10);
    defer {
        for (words) |w| allocator.free(w);
        allocator.free(words);
    }
    std.debug.print("Words starting with 'app':\n", .{});
    for (words) |word| {
        std.debug.print("  - {s}\n", .{word});
    }
    std.debug.print("\n", .{});

    // Longest common prefix
    std.debug.print("--- Longest Common Prefix ---\n", .{});
    var trie2 = try Trie(256).init(allocator);
    defer trie2.deinit();
    _ = try trie2.insert("flower");
    _ = try trie2.insert("flow");
    _ = try trie2.insert("flight");
    var lcp_buf: [256]u8 = undefined;
    const lcp_len = trie2.longestCommonPrefix(&lcp_buf);
    std.debug.print("LCP of 'flower', 'flow', 'flight': {s}\n", .{lcp_buf[0..lcp_len]});
    std.debug.print("\n", .{});

    // Delete operation
    std.debug.print("--- Delete Operation ---\n", .{});
    std.debug.print("Before delete: search 'apple' = {}\n", .{trie.search("apple")});
    const deleted = trie.delete("apple");
    std.debug.print("Delete 'apple': {}\n", .{deleted});
    std.debug.print("After delete: search 'apple' = {}\n", .{trie.search("apple")});
    std.debug.print("Total words now: {}\n", .{trie.count()});

    // Memory info
    std.debug.print("\n--- Memory Info ---\n", .{});
    std.debug.print("Node count: {}\n", .{trie.nodeCount()});
    std.debug.print("Memory usage: {} bytes\n", .{trie.memoryUsage()});
}