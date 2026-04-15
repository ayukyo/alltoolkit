const std = @import("std");
const string_utils = @import("string_utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== Zig String Utils Examples ===\n\n", .{});

    // Trim functions
    std.debug.print("--- Trim Functions ---\n", .{});
    {
        const trimmed = try string_utils.trim(allocator, "   hello world   ");
        defer allocator.free(trimmed);
        std.debug.print("trim('   hello world   ') = '{s}'\n", .{trimmed});
        
        const left_trimmed = try string_utils.trimLeft(allocator, "   hello world   ");
        defer allocator.free(left_trimmed);
        std.debug.print("trimLeft('   hello world   ') = '{s}'\n", .{left_trimmed});
        
        const right_trimmed = try string_utils.trimRight(allocator, "   hello world   ");
        defer allocator.free(right_trimmed);
        std.debug.print("trimRight('   hello world   ') = '{s}'\n", .{right_trimmed});
        
        const custom_trimmed = try string_utils.trimChars(allocator, "xxhello worldxx", "x");
        defer allocator.free(custom_trimmed);
        std.debug.print("trimChars('xxhello worldxx', 'x') = '{s}'\n", .{custom_trimmed});
    }

    std.debug.print("\n", .{});

    // Case conversion
    std.debug.print("--- Case Conversion ---\n", .{});
    {
        const upper = try string_utils.toUpper(allocator, "hello world");
        defer allocator.free(upper);
        std.debug.print("toUpper('hello world') = '{s}'\n", .{upper});
        
        const lower = try string_utils.toLower(allocator, "HELLO WORLD");
        defer allocator.free(lower);
        std.debug.print("toLower('HELLO WORLD') = '{s}'\n", .{lower});
        
        const cap = try string_utils.capitalize(allocator, "hello world");
        defer allocator.free(cap);
        std.debug.print("capitalize('hello world') = '{s}'\n", .{cap});
        
        const title_case = try string_utils.title(allocator, "hello world");
        defer allocator.free(title_case);
        std.debug.print("title('hello world') = '{s}'\n", .{title_case});
        
        const swapped = try string_utils.swapCase(allocator, "Hello World");
        defer allocator.free(swapped);
        std.debug.print("swapCase('Hello World') = '{s}'\n", .{swapped});
    }

    std.debug.print("\n", .{});

    // String manipulation
    std.debug.print("--- String Manipulation ---\n", .{});
    {
        const reversed = try string_utils.reverse(allocator, "hello");
        defer allocator.free(reversed);
        std.debug.print("reverse('hello') = '{s}'\n", .{reversed});
        
        const repeated = try string_utils.repeat(allocator, "ab", 3);
        defer allocator.free(repeated);
        std.debug.print("repeat('ab', 3) = '{s}'\n", .{repeated});
        
        const replaced = try string_utils.replace(allocator, "hello world world", "world", "there");
        defer allocator.free(replaced);
        std.debug.print("replace('hello world world', 'world', 'there') = '{s}'\n", .{replaced});
        
        const replaced_n = try string_utils.replaceN(allocator, "a b a b a", "a", "X", 2);
        defer allocator.free(replaced_n);
        std.debug.print("replaceN('a b a b a', 'a', 'X', 2) = '{s}'\n", .{replaced_n});
    }

    std.debug.print("\n", .{});

    // Split and join
    std.debug.print("--- Split and Join ---\n", .{});
    {
        const parts = try string_utils.split(allocator, "apple,banana,cherry", ",");
        defer string_utils.freeSlice(allocator, parts);
        
        std.debug.print("split('apple,banana,cherry', ','):\n", .{});
        for (parts, 0..) |part, i| {
            std.debug.print("  [{d}]: '{s}'\n", .{ i, part });
        }
        
        const whitespace_parts = try string_utils.splitWhitespace(allocator, "  hello   world  ");
        defer string_utils.freeSlice(allocator, whitespace_parts);
        
        std.debug.print("splitWhitespace('  hello   world  '):\n", .{});
        for (whitespace_parts, 0..) |part, i| {
            std.debug.print("  [{d}]: '{s}'\n", .{ i, part });
        }
        
        const join_parts = [_][]const u8{ "red", "green", "blue" };
        const joined = try string_utils.join(allocator, &join_parts, ", ");
        defer allocator.free(joined);
        std.debug.print("join(['red', 'green', 'blue'], ', ') = '{s}'\n", .{joined});
    }

    std.debug.print("\n", .{});

    // Padding
    std.debug.print("--- Padding ---\n", .{});
    {
        const left_padded = try string_utils.padLeft(allocator, "42", '0', 5);
        defer allocator.free(left_padded);
        std.debug.print("padLeft('42', '0', 5) = '{s}'\n", .{left_padded});
        
        const right_padded = try string_utils.padRight(allocator, "42", '-', 5);
        defer allocator.free(right_padded);
        std.debug.print("padRight('42', '-', 5) = '{s}'\n", .{right_padded});
        
        const centered = try string_utils.center(allocator, "hi", '-', 6);
        defer allocator.free(centered);
        std.debug.print("center('hi', '-', 6) = '{s}'\n", .{centered});
    }

    std.debug.print("\n", .{});

    // Prefix and suffix
    std.debug.print("--- Prefix and Suffix ---\n", .{});
    {
        std.debug.print("startsWith('hello world', 'hello') = {}\n", .{string_utils.startsWith("hello world", "hello")});
        std.debug.print("endsWith('hello world', 'world') = {}\n", .{string_utils.endsWith("hello world", "world")});
        
        const no_prefix = try string_utils.removePrefix(allocator, "hello world", "hello ");
        defer allocator.free(no_prefix);
        std.debug.print("removePrefix('hello world', 'hello ') = '{s}'\n", .{no_prefix});
        
        const no_suffix = try string_utils.removeSuffix(allocator, "hello world", " world");
        defer allocator.free(no_suffix);
        std.debug.print("removeSuffix('hello world', ' world') = '{s}'\n", .{no_suffix});
    }

    std.debug.print("\n", .{});

    // Counting
    std.debug.print("--- Counting ---\n", .{});
    {
        std.debug.print("count('hello hello', 'hello') = {d}\n", .{string_utils.count("hello hello", "hello")});
        std.debug.print("countChar('hello', 'l') = {d}\n", .{string_utils.countChar("hello", 'l')});
    }

    std.debug.print("\n", .{});

    // Character classification
    std.debug.print("--- Character Classification ---\n", .{});
    {
        std.debug.print("isAlpha('hello') = {}\n", .{string_utils.isAlpha("hello")});
        std.debug.print("isAlpha('hello123') = {}\n", .{string_utils.isAlpha("hello123")});
        std.debug.print("isDigit('12345') = {}\n", .{string_utils.isDigit("12345")});
        std.debug.print("isAlnum('hello123') = {}\n", .{string_utils.isAlnum("hello123")});
        std.debug.print("isWhitespace('   ') = {}\n", .{string_utils.isWhitespace("   ")});
        std.debug.print("isLower('hello') = {}\n", .{string_utils.isLower("hello")});
        std.debug.print("isUpper('HELLO') = {}\n", .{string_utils.isUpper("HELLO")});
        std.debug.print("isBlank('') = {}\n", .{string_utils.isBlank("")});
    }

    std.debug.print("\n", .{});

    // Word wrap
    std.debug.print("--- Word Wrap ---\n", .{});
    {
        const wrapped = try string_utils.wordWrap(allocator, "This is a long sentence that needs to be wrapped at a certain width.", 20);
        defer allocator.free(wrapped);
        std.debug.print("wordWrap(long text, 20):\n{s}\n", .{wrapped});
    }

    std.debug.print("\n=== All examples completed ===\n", .{});
}