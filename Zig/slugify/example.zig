const std = @import("std");
const slugify = @import("slugify.zig");

pub fn main() !void {
    // Use GPA for memory allocation
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const stdout = std.io.getStdOut().writer();

    // Example 1: Basic slugify
    try stdout.print("=== Basic Slugify Examples ===\n\n", .{});

    const examples = [_][]const u8{
        "Hello World",
        "This is a Test Article",
        "My Blog Post Title!",
        "Special @#$ Characters Here",
        "Multiple   Spaces   Between",
        "Article 123: The Great Adventure",
    };

    for (examples) |example| {
        const result = try slugify.slugifySimple(allocator, example);
        defer allocator.free(result);
        try stdout.print("  \"{s}\" -> \"{s}\"\n", .{ example, result });
    }

    // Example 2: Custom separator
    try stdout.print("\n=== Custom Separator ===\n\n", .{});

    const underscore_result = try slugify.slugifyWithSeparator(allocator, "Hello World Test", "_");
    defer allocator.free(underscore_result);
    try stdout.print("  With underscore: \"{s}\"\n", .{underscore_result});

    const dot_result = try slugify.slugifyWithSeparator(allocator, "Hello World Test", ".");
    defer allocator.free(dot_result);
    try stdout.print("  With dot: \"{s}\"\n", .{dot_result});

    // Example 3: Max length
    try stdout.print("\n=== Max Length Limit ===\n\n", .{});

    const long_title = "This is a very long article title that should be truncated";
    const truncated = try slugify.slugifyWithMaxLength(allocator, long_title, 30);
    defer allocator.free(truncated);
    try stdout.print("  Original: \"{s}\"\n", .{long_title});
    try stdout.print("  Truncated: \"{s}\" (len={d})\n", .{ truncated, truncated.len });

    // Example 4: Custom options
    try stdout.print("\n=== Custom Options ===\n\n", .{});

    const custom_options = slugify.SlugifyOptions{
        .separator = "~",
        .lowercase = false,
        .remove_duplicates = true,
        .trim_separator = true,
    };

    const custom_result = try slugify.slugify(allocator, "Hello World Custom", custom_options);
    defer allocator.free(custom_result);
    try stdout.print("  Custom separator '~', preserve case: \"{s}\"\n", .{custom_result});

    // Example 5: Validation
    try stdout.print("\n=== Slug Validation ===\n\n", .{});

    const test_slugs = [_][]const u8{
        "hello-world",
        "hello_world",
        "hello world",
        "hello-world-123",
        "Hello-World",
        "",
    };

    for (test_slugs) |test_slug| {
        const is_valid = slugify.isValidSlug(test_slug);
        try stdout.print("  \"{s}\" is {s}valid\n", .{ test_slug, if (is_valid) "" else "not " });
    }

    // Example 6: Parse slug
    try stdout.print("\n=== Parse Slug ===\n\n", .{});

    const parsed_words = try slugify.parseSlug(allocator, "hello-world-from-slug", "-");
    defer {
        for (parsed_words) |word| allocator.free(word);
        allocator.free(parsed_words);
    }

    try stdout.print("  Parsed words from \"hello-world-from-slug\":\n", .{});
    for (parsed_words, 0..) |word, i| {
        try stdout.print("    {d}. {s}\n", .{ i + 1, word });
    }

    // Example 7: Latin-1 accented characters
    try stdout.print("\n=== Latin-1 Character Transliteration ===\n\n", .{});

    // Create Latin-1 encoded strings
    var cafe_input = [_]u8{ 0x63, 0x61, 0x66, 0xE9 }; // café
    const cafe_result = try slugify.slugifySimple(allocator, &cafe_input);
    defer allocator.free(cafe_result);
    try stdout.print("  café (cafe with accent) -> \"{s}\"\n", .{cafe_result});

    var strasse_input = [_]u8{ 0x53, 0x74, 0x72, 0x61, 0xDF, 0x65 }; // Straße
    const strasse_result = try slugify.slugifySimple(allocator, &strasse_input);
    defer allocator.free(strasse_result);
    try stdout.print("  Straße (German sharp-s) -> \"{s}\"\n", .{strasse_result});

    try stdout.print("\n=== Done! ===\n", .{});
}