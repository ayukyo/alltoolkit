# CSV Utils for Zig

A comprehensive CSV parsing and writing library for Zig with zero external dependencies.

## Features

- **CSV Parsing**: Parse CSV strings into records with full support for:
  - Standard CSV format (RFC 4180)
  - Quoted fields with proper escape handling
  - Custom delimiters (comma, semicolon, tab, etc.)
  - Comment line skipping
  - Field count validation
  - Whitespace trimming options

- **CSV Writing**: Generate CSV output with:
  - Automatic quoting when necessary
  - Always-quote option
  - Custom delimiters
  - Custom line endings

- **Type Conversion**: Built-in helpers for converting fields to:
  - Integer (`asInt`)
  - Float (`asFloat`)
  - Boolean (`asBool`)

- **Memory Efficient**: Streaming parser design with proper memory management

## Quick Start

```zig
const std = @import("std");
const csv = @import("csv_utils");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    // Parse CSV
    const input = "name,age,city\nAlice,30,Beijing\nBob,25,Shanghai";
    var records = try csv.parseDefault(allocator, input);
    defer csv.freeRecords(allocator, records);

    // Access fields
    for (records) |record| {
        std.debug.print("Name: {s}, Age: {}\n", .{
            record.get(0).?,
            record.asInt(1).?,
        });
    }
}
```

## API Reference

### Parsing

```zig
// Parse with default options (comma delimiter, double-quote)
var records = try csv.parseDefault(allocator, input);
defer csv.freeRecords(allocator, records);

// Parse with custom options
var records = try csv.parse(allocator, input, .{
    .delimiter = ';',        // Use semicolon
    .quote = '"',            // Quote character
    .comment = '#',          // Skip comment lines
    .trim_leading = true,    // Trim leading whitespace
    .trim_trailing = true,   // Trim trailing whitespace
    .expected_fields = 3,    // Validate field count
});
```

### CsvRecord Methods

```zig
const field = record.get(0);        // Get field at index (returns optional)
const count = record.count();       // Get field count
const num = record.asInt(1);        // Parse as integer (returns optional)
const flt = record.asFloat(2);      // Parse as float (returns optional)
const bool = record.asBool(3);      // Parse as boolean (returns optional)
```

### Writing

```zig
var writer = csv.CsvWriter.init(allocator, .{
    .delimiter = ',',
    .always_quote = false,
    .line_ending = "\n",
});
defer writer.deinit();

try writer.writeHeader(&[_][]const u8{"name", "age", "city"});
try writer.writeRecord(&[_][]const u8{"Alice", "30", "Beijing"});

const output = try writer.toOwnedSlice();
defer allocator.free(output);
```

### Convenience Functions

```zig
// Quick count without full parsing
const count = csv.countRecords(input, .{});

// Parse to 2D array
var arr = try csv.parseToArray(allocator, input, .{});
defer csv.freeArray(allocator, arr);

// Write records directly
const output = try csv.writeDefault(allocator, records);
```

## Options

### ParseOptions

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `delimiter` | u8 | `,` | Field delimiter character |
| `quote` | u8 | `"` | Quote character |
| `escape` | u8 | `"` | Escape character for quotes |
| `comment` | u8 | `0` | Comment line prefix (0 to disable) |
| `trim_leading` | bool | `false` | Trim leading whitespace |
| `trim_trailing` | bool | `false` | Trim trailing whitespace |
| `skip_empty_lines` | bool | `true` | Skip empty lines |
| `expected_fields` | usize | `0` | Expected field count (0 for any) |

### WriteOptions

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `delimiter` | u8 | `,` | Field delimiter character |
| `quote` | u8 | `"` | Quote character |
| `always_quote` | bool | `false` | Always quote all fields |
| `quote_delimiter` | bool | `true` | Quote fields containing delimiter |
| `quote_quote` | bool | `true` | Quote fields containing quote char |
| `quote_newline` | bool | `true` | Quote fields containing newlines |
| `include_header` | bool | `true` | Include header row |
| `line_ending` | []const u8 | `"\n"` | Line ending sequence |

## Error Handling

```zig
pub const CsvError = error{
    OutOfMemory,      // Memory allocation failed
    InvalidFormat,    // Invalid CSV format
    UnclosedQuote,    // Quote not properly closed
    BufferTooSmall,   // Buffer too small
    InvalidEscape,    // Invalid escape sequence
    FieldCountMismatch, // Field count doesn't match expected
};
```

## Boolean Parsing

The `asBool` method recognizes these values:
- **True**: `true`, `TRUE`, `1`, `yes`, `YES`
- **False**: `false`, `FALSE`, `0`, `no`, `NO`

## Testing

Run the tests:

```bash
zig build test
```

Run the example:

```bash
zig build run
```

## License

MIT License - Part of the AllToolkit project.