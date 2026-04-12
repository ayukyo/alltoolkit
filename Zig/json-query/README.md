# JSON Query Tool (Zig)

A fast, zero-dependency JSON parser and query tool written in Zig. Supports JSONPath-style queries for extracting data from JSON documents.

## Features

- **Zero External Dependencies** - Pure Zig implementation
- **Full JSON Parsing** - Objects, arrays, strings, numbers, booleans, null
- **JSONPath-style Queries** - Extract data with path expressions
- **Deep Key Search** - Find all occurrences of a key recursively
- **Memory Safe** - Proper allocation and deallocation
- **100% Test Coverage** - Comprehensive unit tests

## Installation

```bash
# Clone and build
git clone <repo>
cd Zig/json-query
zig build -Doptimize=ReleaseFast
```

The binary will be at `zig-out/bin/json-query`.

## Usage

### Command Line

```bash
# Query JSON file
json-query data.json $.users[0].name

# Parse and pretty-print JSON
json-query --parse data.json

# Find all values with a key (deep search)
json-query --find data.json name
```

### Path Syntax

| Syntax | Description | Example |
|--------|-------------|---------|
| `$.key` | Get object property | `$.name` |
| `$[0]` | Get array element by index | `$[0]` |
| `$.key[0]` | Nested access | `$.users[0].name` |
| `$.*` | All object values | `$.*` |
| `$[*]` | All array elements | `$[*]` |

### Library Usage

```zig
const std = @import("std");
const json_query = @import("json-query");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    // Parse JSON
    const input = \\{"users": [{"name": "Alice", "age": 30}]}
    ;
    var parser = json_query.JsonParser.init(allocator, input);
    var root = try parser.parse();
    defer root.deinit(allocator);

    // Query data
    var engine = json_query.JsonQuery.init(allocator);
    if (try engine.query(root, "$.users[0].name")) |result| {
        std.debug.print("Name: {s}\n", .{result.asString().?});
    }

    // Deep search for all 'name' keys
    var names = try engine.findKey(root, "name");
    defer names.deinit(allocator);
}
```

## API Reference

### JsonValue

```zig
pub const JsonValue = union(enum) {
    null: void,
    bool: bool,
    integer: i64,
    float: f64,
    string: []const u8,
    array: []JsonValue,
    object: std.StringHashMap(JsonValue),

    // Methods
    pub fn deinit(self: *JsonValue, allocator: std.mem.Allocator) void;
    pub fn getType(self: JsonValue) []const u8;
    pub fn asString(self: JsonValue) ?[]const u8;
    pub fn asInt(self: JsonValue) ?i64;
    pub fn asFloat(self: JsonValue) ?f64;
    pub fn asBool(self: JsonValue) ?bool;
    pub fn asArray(self: JsonValue) ?[]JsonValue;
    pub fn asObject(self: JsonValue) ?*std.StringHashMap(JsonValue);
    pub fn get(self: JsonValue, key: []const u8) ?JsonValue;
    pub fn atIndex(self: JsonValue, index: usize) ?JsonValue;
};
```

### JsonParser

```zig
pub const JsonParser = struct {
    pub fn init(allocator: std.mem.Allocator, input: []const u8) JsonParser;
    pub fn parse(self: *JsonParser) !JsonValue;
};
```

### JsonQuery

```zig
pub const JsonQuery = struct {
    pub fn init(allocator: std.mem.Allocator) JsonQuery;
    pub fn query(self: JsonQuery, root: JsonValue, path: []const u8) !?JsonValue;
    pub fn findKey(self: JsonQuery, root: JsonValue, key: []const u8) !JsonValue;
};
```

## Examples

### Basic Queries

```bash
# Create test data
echo '{"name": "Alice", "age": 30}' > test.json
json-query test.json $.name
# Output: "Alice"

json-query test.json $.age
# Output: 30
```

### Nested Objects

```bash
echo '{"user": {"profile": {"name": "Bob"}}}' > nested.json
json-query nested.json $.user.profile.name
# Output: "Bob"
```

### Array Access

```bash
echo '{"items": ["apple", "banana", "cherry"]}' > array.json
json-query array.json $.items[1]
# Output: "banana"
```

### Complex Data

```bash
cat > users.json << 'EOF'
{
  "users": [
    {"name": "Alice", "age": 30, "active": true},
    {"name": "Bob", "age": 25, "active": false},
    {"name": "Charlie", "age": 35, "active": true}
  ],
  "total": 3
}
EOF

json-query users.json $.users[0].name
# Output: "Alice"

json-query --find users.json name
# Output: ["Alice", "Bob", "Charlie"]

json-query --parse users.json
# Pretty-prints the entire JSON
```

## Running Tests

```bash
zig build test
```

## Performance

- **Fast Parsing** - Single-pass parser with minimal allocations
- **Zero Copy Where Possible** - String values reference original input when escaped characters aren't present
- **Efficient Memory** - Uses Zig's allocator pattern for predictable memory management

## License

MIT License