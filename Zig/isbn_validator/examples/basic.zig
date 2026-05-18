const std = @import("std");
const isbn = @import("isbn_validator");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    const allocator = std.heap.page_allocator;

    try stdout.print("=== ISBN Validator Examples ===\n\n", .{});

    // Example 1: Validate ISBN-10
    try stdout.print("1. Validating ISBN-10:\n", .{});
    const isbn10_valid = "0-306-40615-2";
    try stdout.print("   Input: {s}\n", .{isbn10_valid});
    if (isbn.isValidIsbn(isbn10_valid)) {
        try stdout.print("   ✓ Valid ISBN-10\n", .{});
        const parsed = try isbn.Isbn.parse(allocator, isbn10_valid);
        defer parsed.deinit();
        try stdout.print("   Type: {s}\n", .{switch (parsed.type) {
            .isbn10 => "ISBN-10",
            .isbn13 => "ISBN-13",
            .unknown => "Unknown",
        }});
    }

    // Example 2: Validate ISBN-13
    try stdout.print("\n2. Validating ISBN-13:\n", .{});
    const isbn13_valid = "978-0-306-40615-7";
    try stdout.print("   Input: {s}\n", .{isbn13_valid});
    if (isbn.isValidIsbn(isbn13_valid)) {
        try stdout.print("   ✓ Valid ISBN-13\n", .{});
    }

    // Example 3: Invalid ISBN
    try stdout.print("\n3. Invalid ISBN (wrong checksum):\n", .{});
    const isbn_invalid = "0-306-40615-3";
    try stdout.print("   Input: {s}\n", .{isbn_invalid});
    if (!isbn.isValidIsbn(isbn_invalid)) {
        try stdout.print("   ✗ Invalid ISBN\n", .{});
    }

    // Example 4: ISBN with X check digit
    try stdout.print("\n4. ISBN-10 with X check digit:\n", .{});
    const isbn_x = "0-8044-2957-X";
    try stdout.print("   Input: {s}\n", .{isbn_x});
    if (isbn.isValidIsbn(isbn_x)) {
        try stdout.print("   ✓ Valid ISBN-10 (X = 10)\n", .{});
    }

    // Example 5: Convert ISBN-10 to ISBN-13
    try stdout.print("\n5. Converting ISBN-10 to ISBN-13:\n", .{});
    const isbn10_convert = try isbn.Isbn.parse(allocator, "0-306-40615-2");
    defer isbn10_convert.deinit();
    try stdout.print("   Original: {s}\n", .{isbn10_convert.digits});

    const isbn13_converted = try isbn10_convert.toIsbn13(allocator);
    defer isbn13_converted.deinit();
    const formatted = try isbn13_converted.formatHyphens(allocator);
    defer allocator.free(formatted);
    try stdout.print("   Converted: {s}\n", .{formatted});

    // Example 6: Convert ISBN-13 to ISBN-10
    try stdout.print("\n6. Converting ISBN-13 to ISBN-10:\n", .{});
    const isbn13_convert = try isbn.Isbn.parse(allocator, "978-0-306-40615-7");
    defer isbn13_convert.deinit();

    const isbn10_converted = try isbn13_convert.toIsbn10(allocator);
    defer isbn10_converted.deinit();
    try stdout.print("   Original: 978-0-306-40615-7\n", .{});
    try stdout.print("   Converted: {s}\n", .{isbn10_converted.digits});

    // Example 7: Detect ISBN type
    try stdout.print("\n7. Detecting ISBN types:\n", .{});
    const test_inputs = [_][]const u8{
        "0-306-40615-2",
        "978-0-306-40615-7",
        "invalid-isbn",
        "12345",
    };

    for (test_inputs) |input| {
        const isbn_type = isbn.detectIsbnType(input);
        const type_str = switch (isbn_type) {
            .isbn10 => "ISBN-10",
            .isbn13 => "ISBN-13",
            .unknown => "Unknown",
        };
        try stdout.print("   {s}: {s}\n", .{ input, type_str });
    }

    // Example 8: Calculate check digits
    try stdout.print("\n8. Calculating check Digits:\n", .{});

    const isbn10_base = "030640615";
    const check10 = try isbn.calculateIsbn10CheckDigit(isbn10_base);
    try stdout.print("   ISBN-10 base: {s}\n", .{isbn10_base});
    try stdout.print("   Check digit: {c}\n", .{check10});
    try stdout.print("   Complete: {s}{c}\n", .{ isbn10_base, check10 });

    const isbn13_base = "978030640615";
    const check13 = try isbn.calculateIsbn13CheckDigit(isbn13_base);
    try stdout.print("\n   ISBN-13 base: {s}\n", .{isbn13_base});
    try stdout.print("   Check digit: {c}\n", .{check13});
    try stdout.print("   Complete: {s}{c}\n", .{ isbn13_base, check13 });

    // Example 9: Parse without allocation (static)
    try stdout.print("\n9. Static parsing (no allocation):\n", .{});
    const static_isbn = isbn.Isbn.parseStatic("978-1-56619-909-4") catch {
        try stdout.print("   Failed to parse\n", .{});
        return;
    };
    try stdout.print("   Input: 978-1-56619-909-4\n", .{});
    try stdout.print("   Valid: {}\n", .{static_isbn.isValid()});

    try stdout.print("\n=== Examples Complete ===\n", .{});
}