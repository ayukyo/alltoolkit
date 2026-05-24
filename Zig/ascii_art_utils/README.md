# ASCII Art Utils for Zig

A lightweight, zero-dependency ASCII art generator for Zig. Convert text to ASCII art using multiple font styles.

## Features

- 🎨 **4 Font Styles**: Standard, Banner, Mini, Slant
- 📦 **Zero Dependencies**: Pure Zig implementation
- ⚡ **Fast & Efficient**: Compile-time font definitions
- 🔧 **Easy to Use**: Simple API for generating ASCII art
- ✅ **Fully Tested**: Comprehensive test suite included

## Installation

Copy `ascii_art.zig` to your project and import it:

```zig
const ascii_art = @import("ascii_art.zig");
```

## Usage

### Basic Usage

```zig
const std = @import("std");
const ascii_art = @import("ascii_art.zig");

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    
    // Generate ASCII art
    const art = try ascii_art.generateAscii(allocator, "HELLO", .standard);
    defer allocator.free(art);
    
    std.debug.print("{s}\n", .{art});
}
```

### Using Different Fonts

```zig
const ascii_art = @import("ascii_art.zig");

// Available fonts: standard, banner, mini, slant
const art1 = try ascii_art.generateAscii(allocator, "ZIG", .standard);
const art2 = try ascii_art.generateAscii(allocator, "ZIG", .banner);
const art3 = try ascii_art.generateAscii(allocator, "ZIG", .mini);
const art4 = try ascii_art.generateAscii(allocator, "ZIG", .slant);
```

### Using AsciiArt Struct

```zig
const std = @import("std");
const ascii_art = @import("ascii_art.zig");

pub fn main() !void {
    var art = ascii_art.AsciiArt.init(std.heap.page_allocator, .standard);
    
    const result = try art.generate("Hello World!");
    defer std.heap.page_allocator.free(result);
    
    std.debug.print("{s}\n", .{result});
}
```

### Print to Stdout

```zig
const ascii_art = @import("ascii_art.zig");

try ascii_art.printAscii("HELLO", .standard);
```

### Parse Font Name

```zig
const font = ascii_art.parseFontName("slant");
if (font) |f| {
    const art = try ascii_art.generateAscii(allocator, "TEXT", f);
}
```

## Font Examples

### Standard Font
```
  ##   ###  ###   ###
 #       # #   # #
 ###    #  #   # #
 #      #  #   # #
 ####  ###  ###   ###
```

### Banner Font
```
 ###  ###  ### 
 #    #  # #   
 ###  ###  ### 
 #    #  #   # 
 ###  ###  ###
```

### Mini Font
```
 #  ##  ##
##  #  # 
#   ##  #
```

### Slant Font (Italic Style)
```
   ##    ###   ###    ###
  #      #     #   # #   
 ###    #     #   # #   
#      #     #   # #   
#####  ###   ###    ###
```

## API Reference

### Types

```zig
pub const Font = enum {
    standard,  // 6 lines height, full ASCII characters
    banner,    // 5 lines height, block style
    mini,      // 3 lines height, compact
    slant,     // 6 lines height, italic style
};
```

### Functions

```zig
/// Generate ASCII art from text (convenience function)
pub fn generateAscii(allocator: std.mem.Allocator, text: []const u8, font: Font) ![]u8

/// Print ASCII art to stdout
pub fn printAscii(text: []const u8, font: Font) !void

/// Get list of available fonts
pub fn getAvailableFonts() []const []const u8

/// Parse font name to Font enum
pub fn parseFontName(name: []const u8) ?Font
```

### AsciiArt Struct

```zig
pub const AsciiArt = struct {
    /// Initialize with allocator and font
    pub fn init(allocator: std.mem.Allocator, font: Font) Self
    
    /// Generate ASCII art from text
    pub fn generate(self: *Self, text: []const u8) ![]u8
    
    /// Free resources
    pub fn deinit(self: *Self) void
};
```

## Supported Characters

- Uppercase letters: A-Z
- Lowercase letters: a-z
- Numbers: 0-9
- Special characters: ! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ ` { | } ~
- Space character

## Running Tests

```bash
zig test ascii_art.zig
```

## Example Output

```
Input:  HELLO
Font:   standard

  ##   ###  ###   ###
 #       # #   # #
 ###    #  #   # ###
 #      #  #   # # #
 ####  ###  ###   ###
```

## License

MIT License - Feel free to use in your projects!

## Contributing

Contributions welcome! Feel free to add more fonts or features.

## Notes

- All fonts are defined at compile time for maximum performance
- The generator handles multiline text
- Unknown characters are skipped silently
- Memory is managed by the caller (remember to free the result)