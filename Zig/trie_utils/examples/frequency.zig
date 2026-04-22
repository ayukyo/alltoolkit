const std = @import("std");
const Trie = @import("trie").Trie;

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== Word Frequency Analysis Example ===\n\n", .{});

    // Create a trie to store unique words
    var trie = try Trie(256).init(allocator);
    defer trie.deinit();

    // Sample text - a paragraph
    const text = 
        \\The quick brown fox jumps over the lazy dog. 
        \\The dog barks at the fox but the fox is too quick.
        \\Quick thinking helps the fox escape from the dog.
        \\The lazy dog sleeps while the fox runs around.
    ;

    std.debug.print("Sample text:\n{s}\n\n", .{text});

    // Split text into words and count frequency
    var word_counts = std.StringHashMap(usize).init(allocator);
    defer {
        var iter = word_counts.iterator();
        while (iter.next()) |entry| {
            allocator.free(entry.key_ptr.*);
        }
        word_counts.deinit();
    }

    // Process each word
    var words_iter = std.mem.tokenizeAny(u8, text, " \t\n\r.,!?;:'\"()[]{}");
    var total_words: usize = 0;
    var unique_words: usize = 0;

    while (words_iter.next()) |raw_word| {
        total_words += 1;

        // Convert to lowercase
        var word_buf: [256]u8 = undefined;
        const word = toLower(raw_word, &word_buf);

        // Try to add to trie
        const is_new = try trie.insert(word);
        if (is_new) {
            unique_words += 1;
        }

        // Update frequency count
        const gop = try word_counts.getOrPut(try allocator.dupe(u8, word));
        if (gop.found_existing) {
            gop.value_ptr.* += 1;
        } else {
            gop.value_ptr.* = 1;
        }
    }

    std.debug.print("--- Word Statistics ---\n", .{});
    std.debug.print("Total words: {}\n", .{total_words});
    std.debug.print("Unique words: {}\n", .{unique_words});
    std.debug.print("Trie node count: {}\n", .{trie.nodeCount()});
    std.debug.print("Estimated memory: {} bytes\n\n", .{trie.memoryUsage()});

    // Show all unique words from trie
    std.debug.print("--- All Unique Words (from Trie) ---\n", .{});
    const all_words = try trie.getAllWords(allocator);
    defer {
        for (all_words) |w| allocator.free(w);
        allocator.free(all_words);
    }

    // Sort words alphabetically for display
    std.sort.pdq([]u8, all_words, {}, struct {
        fn lessThan(_: void, a: []u8, b: []u8) bool {
            return std.mem.lessThan(u8, a, b);
        }
    }.lessThan);

    for (all_words) |word| {
        const count = word_counts.get(word) orelse 0;
        std.debug.print("  {s}: {}\n", .{ word, count });
    }

    // Find common prefixes
    std.debug.print("\n--- Prefix Analysis ---\n", .{});
    const prefixes = [_][]const u8{ "th", "qu", "do", "fo", "br" };
    for (prefixes) |prefix| {
        const count = trie.countPrefix(prefix);
        if (count > 0) {
            std.debug.print("Words starting with '{s}': {}\n", .{ prefix, count });
            const words = try trie.getWordsWithPrefix(allocator, prefix, 5);
            defer {
                for (words) |w| allocator.free(w);
                allocator.free(words);
            }
            for (words) |word| {
                const freq = word_counts.get(word) orelse 0;
                std.debug.print("  - {s} ({})\n", .{ word, freq });
            }
            std.debug.print("\n", .{});
        }
    }

    std.debug.print("--- Benefits of Using Trie ---\n", .{});
    std.debug.print("1. Fast prefix-based lookups (O(n) where n = prefix length)\n", .{});
    std.debug.print("2. Memory efficient for shared prefixes\n", .{});
    std.debug.print("3. Autocomplete-friendly data structure\n", .{});
    std.debug.print("4. Easy pattern matching with wildcards\n", .{});
}

fn toLower(input: []const u8, buf: *[256]u8) []const u8 {
    var i: usize = 0;
    for (input) |c| {
        if (i >= buf.len - 1) break;
        buf[i] = if (c >= 'A' and c <= 'Z') c + 32 else c;
        i += 1;
    }
    return buf[0..i];
}