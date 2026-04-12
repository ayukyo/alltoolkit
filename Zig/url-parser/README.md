# URL Parser - Zig

A zero-dependency URL parsing and building library for Zig. Provides comprehensive URL parsing, construction, and manipulation capabilities.

## Features

- **URL Parsing**: Parse URLs into components (scheme, host, port, path, query, fragment, credentials)
- **URL Building**: Construct URLs programmatically with a fluent builder API
- **Query String Handling**: Parse and manipulate query parameters
- **Percent Encoding/Decoding**: URL-safe encoding and decoding
- **Path Utilities**: Join paths, extract filenames and extensions
- **IPv6 Support**: Full support for IPv6 host addresses
- **Default Port Resolution**: Automatic default port lookup for common schemes
- **Security Checks**: Verify if URLs use secure schemes (https, wss)

## Installation

Add to your `build.zig.zon`:

```zig
.{
    .name = "your-project",
    .version = "0.1.0",
    .dependencies = .{
        .url_parser = .{
            .path = "path/to/url-parser",
        },
    },
}
```

Or copy the `src/main.zig` file to your project.

## Quick Start

```zig
const std = @import("std");
const url = @import("url");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    // Parse a URL
    var parsed = try url.Url.parse(allocator, "https://api.example.com/v1/users?page=1");
    defer parsed.deinit();

    std.debug.print("Host: {s}\n", .{parsed.host});
    std.debug.print("Path: {s}\n", .{parsed.path});
    std.debug.print("Query: {s}\n", .{parsed.query});
}
```

## API Reference

### Url (Parsing)

```zig
const Url = struct {
    scheme: []const u8,
    host: []const u8,
    port: ?u16,
    path: []const u8,
    query: []const u8,
    fragment: []const u8,
    username: []const u8,
    password: []const u8,

    pub fn parse(allocator: Allocator, url_str: []const u8) UrlError!Url;
    pub fn deinit(self: *Url) void;
    pub fn toString(self: Url, allocator: Allocator) ![]const u8;
    pub fn defaultPort(self: Url) u16;
    pub fn isSecure(self: Url) bool;
    pub fn getQueryParams(self: Url, allocator: Allocator) !StringHashMap([]const u8);
};
```

### UrlBuilder (Construction)

```zig
const UrlBuilder = struct {
    pub fn init(allocator: Allocator) UrlBuilder;
    pub fn deinit(self: *UrlBuilder) void;
    pub fn setScheme(self: *UrlBuilder, scheme: []const u8) !void;
    pub fn setHost(self: *UrlBuilder, host: []const u8) !void;
    pub fn setPort(self: *UrlBuilder, port: u16) void;
    pub fn setPath(self: *UrlBuilder, path: []const u8) !void;
    pub fn addQueryParam(self: *UrlBuilder, key: []const u8, value: []const u8) !void;
    pub fn setFragment(self: *UrlBuilder, fragment: []const u8) !void;
    pub fn setCredentials(self: *UrlBuilder, username: []const u8, password: []const u8) !void;
    pub fn build(self: *UrlBuilder) ![]const u8;
};
```

### Utility Functions

```zig
// Percent encode a string for URLs
pub fn percentEncode(allocator: Allocator, input: []const u8) ![]const u8;

// Percent decode a URL-encoded string
pub fn percentDecode(allocator: Allocator, input: []const u8) UrlError![]const u8;

// Join path segments
pub fn joinPath(allocator: Allocator, segments: []const []const u8) ![]const u8;

// Extract file extension from path
pub fn getExtension(path: []const u8) ?[]const u8;

// Extract filename from path
pub fn getFilename(path: []const u8) []const u8;
```

## Examples

### Parse and Extract Components

```zig
var url = try url.Url.parse(allocator, "https://user:pass@api.example.com:8080/v1/search?q=zig#results");
defer url.deinit();

// Components
std.debug.print("Scheme: {s}\n", .{url.scheme});     // "https"
std.debug.print("Host: {s}\n", .{url.host});        // "api.example.com"
std.debug.print("Port: {?}\n", .{url.port});        // 8080
std.debug.print("Username: {s}\n", .{url.username}); // "user"
std.debug.print("Password: {s}\n", .{url.password}); // "pass"
std.debug.print("Path: {s}\n", .{url.path});        // "/v1/search"
std.debug.print("Query: {s}\n", .{url.query});       // "q=zig"
std.debug.print("Fragment: {s}\n", .{url.fragment}); // "results"
```

### Build URLs Programmatically

```zig
var builder = url.UrlBuilder.init(allocator);
defer builder.deinit();

try builder.setScheme("https");
try builder.setHost("api.example.com");
builder.setPort(443);
try builder.setPath("/v1/search");
try builder.addQueryParam("q", "zig");
try builder.addQueryParam("limit", "10");
try builder.setFragment("results");

const result = try builder.build();
defer allocator.free(result);
// result: "https://api.example.com:443/v1/search?q=zig&limit=10#results"
```

### Handle Query Parameters

```zig
var parsed = try url.Url.parse(allocator, "https://example.com?key1=value1&key2=value2");
defer parsed.deinit();

var params = try parsed.getQueryParams(allocator);
defer {
    var iter = params.iterator();
    while (iter.next()) |entry| {
        allocator.free(entry.key_ptr.*);
        allocator.free(entry.value_ptr.*);
    }
    params.deinit();
}

if (params.get("key1")) |value| {
    std.debug.print("key1 = {s}\n", .{value});
}
```

### Percent Encoding

```zig
// Encode
const encoded = try url.percentEncode(allocator, "hello world!");
defer allocator.free(encoded);
// encoded: "hello%20world%21"

// Decode
const decoded = try url.percentDecode(allocator, "hello%20world%21");
defer allocator.free(decoded);
// decoded: "hello world!"
```

### Path Utilities

```zig
// Join paths
const segments = [_][]const u8{ "api", "v1", "users" };
const path = try url.joinPath(allocator, &segments);
defer allocator.free(path);
// path: "api/v1/users"

// Extract filename and extension
const filepath = "/documents/report.pdf";
std.debug.print("Filename: {s}\n", .{url.getFilename(filepath)}); // "report.pdf"
std.debug.print("Extension: {s}\n", .{url.getExtension(filepath).?}); // "pdf"
```

### IPv6 Support

```zig
var ipv6_url = try url.Url.parse(allocator, "http://[::1]:3000/api");
defer ipv6_url.deinit();

std.debug.print("Host: {s}\n", .{ipv6_url.host}); // "[::1]"
std.debug.print("Port: {}\n", .{ipv6_url.port.?}); // 3000
```

## Error Handling

```zig
const result = url.Url.parse(allocator, "invalid-url");
if (result) |parsed| {
    defer parsed.deinit();
    // Success
} else |err| {
    switch (err) {
        url.UrlError.InvalidScheme => std.debug.print("Missing or invalid scheme\n", .{}),
        url.UrlError.InvalidPort => std.debug.print("Invalid port number\n", .{}),
        url.UrlError.InvalidHost => std.debug.print("Invalid host\n", .{}),
        url.UrlError.InvalidPercentEncoding => std.debug.print("Invalid percent encoding\n", .{}),
        else => std.debug.print("Other error: {}\n", .{err}),
    }
}
```

## Building

```bash
# Build the library
zig build

# Run tests
zig build test

# Run basic example
zig build run-basic

# Run advanced example
zig build run-advanced
```

## Supported Schemes with Default Ports

| Scheme | Default Port | Secure |
|--------|-------------|--------|
| http   | 80          | No     |
| https  | 443         | Yes    |
| ws     | 80          | No     |
| wss    | 443         | Yes    |
| ftp    | 21          | No     |
| ssh    | 22          | No     |
| telnet | 23          | No     |
| smtp   | 25          | No     |
| dns    | 53          | No     |

## License

MIT License - Free to use in any project.