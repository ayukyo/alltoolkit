const std = @import("std");
const Trie = @import("trie").Trie;

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== Pattern Matching Example ===\n\n", .{});

    // Create a trie with animal names
    var trie = try Trie(256).init(allocator);
    defer trie.deinit();

    const animals = [_][]const u8{
        "cat",
        "car",
        "card",
        "care",
        "careful",
        "carpet",
        "cart",
        "dog",
        "dot",
        "dove",
        "door",
        "bat",
        "bar",
        "bard",
        "bark",
        "bare",
        "bear",
        "beard",
    };

    std.debug.print("Loading {} animal/word patterns...\n\n", .{animals.len});
    _ = try trie.insertBatch(&animals);

    // Pattern matching with '?' (single character wildcard)
    std.debug.print("--- Single Character Wildcard (?) ---\n", .{});
    std.debug.print("'?' matches any single character\n\n", .{});

    const single_patterns = [_][]const u8{ "ca?", "ba?", "d?g", "?at" };

    for (single_patterns) |pattern| {
        std.debug.print("Pattern '{s}':\n", .{pattern});
        const matches = try trie.patternMatch(allocator, pattern, 10);
        defer {
            for (matches) |m| allocator.free(m);
            allocator.free(matches);
        }
        for (matches) |match| {
            std.debug.print("  - {s}\n", .{match});
        }
        std.debug.print("\n", .{});
    }

    // Pattern matching with '*' (multiple character wildcard)
    std.debug.print("--- Multi-Character Wildcard (*) ---\n", .{});
    std.debug.print("'*' matches zero or more characters\n\n", .{});

    const multi_patterns = [_][]const u8{ "ca*", "ba*", "do*" };

    for (multi_patterns) |pattern| {
        std.debug.print("Pattern '{s}':\n", .{pattern});
        const matches = try trie.patternMatch(allocator, pattern, 10);
        defer {
            for (matches) |m| allocator.free(m);
            allocator.free(matches);
        }
        for (matches) |match| {
            std.debug.print("  - {s}\n", .{match});
        }
        std.debug.print("\n", .{});
    }

    // Combined wildcards
    std.debug.print("--- Combined Wildcards ---\n", .{});
    std.debug.print("Combining ? and * for complex patterns\n\n", .{});

    const combined_patterns = [_][]const u8{ "?a*", "ca?*", "?ar?" };

    for (combined_patterns) |pattern| {
        std.debug.print("Pattern '{s}':\n", .{pattern});
        const matches = try trie.patternMatch(allocator, pattern, 10);
        defer {
            for (matches) |m| allocator.free(m);
            allocator.free(matches);
        }
        for (matches) |match| {
            std.debug.print("  - {s}\n", .{match});
        }
        std.debug.print("\n", .{});
    }

    // Real-world example: Crossword puzzle helper
    std.debug.print("--- Crossword Helper ---\n", .{});
    std.debug.print("Find 5-letter words: '?????'\n", .{});
    std.debug.print("(showing first 10)\n", .{});
    const five_letter = try trie.patternMatch(allocator, "?????", 10);
    defer {
        for (five_letter) |f| allocator.free(f);
        allocator.free(five_letter);
    }
    for (five_letter) |word| {
        std.debug.print("  - {s}\n", .{word});
    }
}