const std = @import("std");
const Trie = @import("trie").Trie;

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== Spell Checker Example ===\n\n", .{});

    // Create a dictionary trie
    var dictionary = try Trie(256).init(allocator);
    defer dictionary.deinit();

    // Add common English words
    const common_words = [_][]const u8{
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
        "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
        "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
        "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
        "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
        "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
        "people", "into", "year", "your", "good", "some", "could", "them", "see", "other",
        "than", "then", "now", "look", "only", "come", "its", "over", "think", "also",
        "back", "after", "use", "two", "how", "our", "work", "first", "well", "way",
        "even", "new", "want", "because", "any", "these", "give", "day", "most", "us",
        "hello", "world", "programming", "computer", "algorithm", "data", "structure",
        "hello", "there", "friend", "welcome", "thank", "please", "sorry", "excuse",
    };

    std.debug.print("Loading dictionary with {} words...\n", .{common_words.len});
    const loaded = try dictionary.insertBatch(&common_words);
    std.debug.print("Dictionary loaded: {} words\n\n", .{loaded});

    // Test words
    const test_words = [_][]const u8{
        "hello",
        "wrld",      // misspelled
        "program",   // prefix of programming
        "world",
        "freind",    // misspelled (friend)
        "thnak",     // misspelled (thank)
        "computer",
        "data",
        "algorithem", // misspelled (algorithm)
    };

    std.debug.print("--- Spell Check Results ---\n", .{});
    for (test_words) |word| {
        const found = dictionary.search(word);
        std.debug.print("'{s}': ", .{word});
        if (found) {
            std.debug.print("✓ correct\n", .{});
        } else {
            std.debug.print("✗ not found", .{});
            
            // Try to find similar words
            const suggestions = dictionary.getWordsWithPrefix(allocator, word[0..@min(3, word.len)], 5) catch &[_][]u8{};
            defer {
                for (suggestions) |s| allocator.free(s);
                allocator.free(suggestions);
            }

            if (suggestions.len > 0) {
                std.debug.print(" - Did you mean: ", .{});
                for (suggestions, 0..) |suggestion, i| {
                    if (i > 0) std.debug.print(", ", .{});
                    std.debug.print("{s}", .{suggestion});
                }
                std.debug.print("?", .{});
            }
            std.debug.print("\n", .{});
        }
    }

    // Demonstrate prefix checking for autocomplete-assisted typing
    std.debug.print("\n--- Prefix Suggestions ---\n", .{});
    std.debug.print("Type 'pro' and see suggestions:\n", .{});
    const pro_suggestions = try dictionary.getWordsWithPrefix(allocator, "pro", 5);
    defer {
        for (pro_suggestions) |s| allocator.free(s);
        allocator.free(pro_suggestions);
    }
    for (pro_suggestions) |suggestion| {
        std.debug.print("  - {s}\n", .{suggestion});
    }

    std.debug.print("\nType 'str' and see suggestions:\n", .{});
    const str_suggestions = try dictionary.getWordsWithPrefix(allocator, "str", 5);
    defer {
        for (str_suggestions) |s| allocator.free(s);
        allocator.free(str_suggestions);
    }
    for (str_suggestions) |suggestion| {
        std.debug.print("  - {s}\n", .{suggestion});
    }
}