const std = @import("std");
const Trie = @import("trie").Trie;

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== Autocomplete Example ===\n\n", .{});

    // Create a trie with programming keywords
    var trie = try Trie(256).init(allocator);
    defer trie.deinit();

    // Insert common programming keywords and functions
    const keywords = [_][]const u8{
        "function",
        "func",
        "for",
        "foreach",
        "format",
        "find",
        "filter",
        "from",
        "if",
        "import",
        "implements",
        "interface",
        "in",
        "is",
        "instanceof",
        "return",
        "require",
        "read",
        "remove",
        "replace",
        "while",
        "write",
        "with",
        "const",
        "class",
        "continue",
        "case",
        "catch",
        "switch",
        "string",
        "struct",
        "static",
    };

    std.debug.print("Loading {} programming keywords...\n", .{keywords.len});
    const inserted = try trie.insertBatch(&keywords);
    std.debug.print("Inserted {} keywords\n\n", .{inserted});

    // Simulate autocomplete suggestions
    const prefixes = [_][]const u8{ "f", "re", "i", "st", "wh", "con" };

    for (prefixes) |prefix| {
        std.debug.print("Autocomplete for '{s}':\n", .{prefix});
        const suggestions = try trie.getWordsWithPrefix(allocator, prefix, 5);
        defer {
            for (suggestions) |s| allocator.free(s);
            allocator.free(suggestions);
        }

        for (suggestions) |suggestion| {
            std.debug.print("  - {s}\n", .{suggestion});
        }
        if (suggestions.len == 0) {
            std.debug.print("  (no suggestions)\n", .{});
        }
        std.debug.print("\n", .{});
    }

    // Demonstrate limiting results
    std.debug.print("--- Limiting Results ---\n", .{});
    std.debug.print("All words starting with 'st' (max 3):\n", .{});
    const limited = try trie.getWordsWithPrefix(allocator, "st", 3);
    defer {
        for (limited) |l| allocator.free(l);
        allocator.free(limited);
    }
    for (limited) |word| {
        std.debug.print("  - {s}\n", .{word});
    }

    // Show total count vs returned
    std.debug.print("\nTotal 'st' words: {}, Returned: {}\n", .{ trie.countPrefix("st"), limited.len });
}