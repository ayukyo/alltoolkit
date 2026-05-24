//! ASCII Art Utils Example
//! 
//! This example demonstrates various ways to use the ASCII art generator.

const std = @import("std");
const ascii_art = @import("ascii_art.zig");

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    const stdout = std.io.getStdOut().writer();
    
    try stdout.print("\n=== ASCII Art Generator Examples ===\n\n", .{});
    
    // Example 1: Standard font
    try stdout.print("1. Standard Font:\n", .{});
    try ascii_art.printAscii("HELLO", .standard);
    try stdout.print("\n", .{});
    
    // Example 2: Banner font
    try stdout.print("2. Banner Font:\n", .{});
    try ascii_art.printAscii("WORLD", .banner);
    try stdout.print("\n", .{});
    
    // Example 3: Mini font (compact)
    try stdout.print("3. Mini Font:\n", .{});
    try ascii_art.printAscii("ZIG", .mini);
    try stdout.print("\n", .{});
    
    // Example 4: Slant font (italic)
    try stdout.print("4. Slant Font:\n", .{});
    try ascii_art.printAscii("ROCKS", .slant);
    try stdout.print("\n", .{});
    
    // Example 5: Numbers
    try stdout.print("5. Numbers with Standard Font:\n", .{});
    try ascii_art.printAscii("2026", .standard);
    try stdout.print("\n", .{});
    
    // Example 6: Mixed case
    try stdout.print("6. Mixed Case:\n", .{});
    try ascii_art.printAscii("Hello World", .standard);
    try stdout.print("\n", .{});
    
    // Example 7: Using generate function (returns string)
    try stdout.print("7. Using generate() function:\n", .{});
    var art_generator = ascii_art.AsciiArt.init(allocator, .banner);
    const generated = try art_generator.generate("PROGRAMMING");
    defer allocator.free(generated);
    try stdout.print("{s}\n", .{generated});
    
    // Example 8: Parse font name
    try stdout.print("8. Parse Font Name:\n", .{});
    const fonts = ascii_art.getAvailableFonts();
    try stdout.print("Available fonts: ", .{});
    for (fonts) |font_name| {
        try stdout.print("{s} ", .{font_name});
    }
    try stdout.print("\n\n", .{});
    
    // Example 9: Special characters
    try stdout.print("9. Special Characters:\n", .{});
    try ascii_art.printAscii("@#$%", .standard);
    try stdout.print("\n", .{});
    
    // Example 10: All fonts comparison
    try stdout.print("10. All Fonts Comparison for 'AB':\n", .{});
    try stdout.print("\n--- Standard ---\n", .{});
    try ascii_art.printAscii("AB", .standard);
    try stdout.print("\n--- Banner ---\n", .{});
    try ascii_art.printAscii("AB", .banner);
    try stdout.print("\n--- Mini ---\n", .{});
    try ascii_art.printAscii("AB", .mini);
    try stdout.print("\n--- Slant ---\n", .{});
    try ascii_art.printAscii("AB", .slant);
    try stdout.print("\n", .{});
    
    try stdout.print("\n=== End of Examples ===\n", .{});
}