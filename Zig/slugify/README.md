# Slugify Utils (Zig)

A lightweight, zero-dependency URL slug generator for Zig. Convert any string into a URL-friendly slug format.

## Features

- **Transliteration**: Automatic conversion of accented characters (é→e, ü→u, etc.)
- **Customizable separators**: Use any separator character(s)
- **Duplicate removal**: Optionally collapse consecutive separators
- **Max length**: Truncate to a maximum length while preserving word boundaries
- **Case control**: Optionally preserve original case
- **Validation**: Check if strings are valid slugs
- **Parsing**: Convert slugs back into word arrays

## Usage

### Basic Usage

```zig
const std = @import("std");
const slugify = @import("slugify.zig");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    // Simple slugify
    const result = try slugify.slugifySimple(allocator, "Hello, World!");
    defer allocator.free(result);
    
    std.debug.print("{s}\n", .{result}); // Output: hello-world
}
```

### Custom Options

```zig
const options = slugify.SlugifyOptions{
    .separator = "_",          // Use underscore instead of hyphen
    .lowercase = true,         // Convert to lowercase
    .remove_duplicates = true,  // Collapse consecutive separators
    .trim_separator = true,     // Remove leading/trailing separators
    .max_length = 50,          // Maximum slug length
};

const result = try slugify.slugify(allocator, "My Article Title!", options);
defer allocator.free(result);
```

### Convenience Functions

```zig
// With custom separator
const result = try slugify.slugifyWithSeparator(allocator, "Hello World", "_");
// Output: hello_world

// With max length
const result = try slugify.slugifyWithMaxLength(allocator, "Very Long Title", 10);
// Output: very-long (truncated)
```

### Validation

```zig
// Check if a string is a valid slug
if (slugify.isValidSlug("hello-world")) {
    // Valid slug
}
```

### Parsing

```zig
// Parse a slug back into words
const words = try slugify.parseSlug(allocator, "hello-world-test", "-");
defer {
    for (words) |word| allocator.free(word);
    allocator.free(words);
}

for (words) |word| {
    std.debug.print("{s}\n", .{word});
}
// Output:
// hello
// world
// test
```

## API Reference

### `slugify(allocator, input, options)`

Convert a string to a URL-friendly slug.

- **allocator**: Memory allocator
- **input**: Input string to convert
- **options**: `SlugifyOptions` struct
- **Returns**: Owned slice (caller must free)

### `slugifySimple(allocator, input)`

Convenience function with default options.

### `slugifyWithSeparator(allocator, input, separator)`

Slugify with a custom separator.

### `slugifyWithMaxLength(allocator, input, max_length)`

Slugify with a maximum length limit.

### `isValidSlug(input) bool`

Check if a string is already a valid slug (alphanumeric, hyphens, underscores only).

### `parseSlug(allocator, slug, separator)`

Parse a slug back into an array of words.

## Transliteration Support

The following accented characters are automatically converted:

| Input | Output |
|-------|--------|
| àáâãäå | a |
| èéêë | e |
| ìíîï | i |
| òóôõöø | o |
| ùúûü | u |
| ýÿ | y |
| ñ | n |
| ç | c |
| ß | ss |
| æ | ae |
| œ | oe |

## Examples

| Input | Output |
|-------|--------|
| `Hello World` | `hello-world` |
| `Café résumé` | `cafe-resume` |
| `Straße für Ärzte` | `strasse-fur-ärzte` |
| `Article 123!` | `article-123` |
| `---test---` | `test` |
| `Multiple   Spaces` | `multiple-spaces` |

## Testing

```bash
cd Zig/slugify
zig test slugify.zig
```

## License

MIT License