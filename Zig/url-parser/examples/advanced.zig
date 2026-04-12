const std = @import("std");
const url = @import("url");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== URL Parser - Advanced Usage ===\n\n", .{});

    // Example 1: Reconstruct and modify URL
    std.debug.print("1. Reconstruct and modify URL:\n", .{});
    const original = "http://example.com/old-path?key=value";
    var parsed = try url.Url.parse(allocator, original);
    defer parsed.deinit();

    std.debug.print("   Original: {s}\n", .{original});

    // Reconstruct
    const reconstructed = try parsed.toString(allocator);
    defer allocator.free(reconstructed);
    std.debug.print("   Reconstructed: {s}\n", .{reconstructed});

    // Create modified version using builder
    var builder = url.UrlBuilder.init(allocator);
    defer builder.deinit();

    try builder.setScheme("https");
    try builder.setHost(parsed.host);
    builder.setPort(443);
    try builder.setPath("/new-path");
    try builder.addQueryParam("key", "new-value");
    try builder.addQueryParam("extra", "param");

    const modified = try builder.build();
    defer allocator.free(modified);
    std.debug.print("   Modified: {s}\n\n", .{modified});

    // Example 2: Parse complex query strings
    std.debug.print("2. Complex query string handling:\n", .{});
    const complex_query_url = "https://search.example.com/results?q=zig+programming&page=1&filters%5Bstatus%5D=active&filters%5Blang%5D=en";
    var complex = try url.Url.parse(allocator, complex_query_url);
    defer complex.deinit();

    std.debug.print("   Raw query: {s}\n", .{complex.query});

    // Decode the query string
    const decoded_query = try url.percentDecode(allocator, complex.query);
    defer allocator.free(decoded_query);
    std.debug.print("   Decoded query: {s}\n\n", .{decoded_query});

    // Example 3: IPv6 URL handling
    std.debug.print("3. IPv6 URL handling:\n", .{});
    const ipv6_urls = [_][]const u8{
        "http://[::1]:3000/api",
        "https://[2001:db8::1]:443/secure",
        "ftp://[fe80::1%eth0]/files",
    };

    for (ipv6_urls) |ipv6_url| {
        var ipv6_parsed = try url.Url.parse(allocator, ipv6_url);
        defer ipv6_parsed.deinit();
        std.debug.print("   {s}\n", .{ipv6_url});
        std.debug.print("      Host: {s}\n", .{ipv6_parsed.host});
        if (ipv6_parsed.port) |p| {
            std.debug.print("      Port: {}\n", .{p});
        }
    }

    // Example 4: URL validation patterns
    std.debug.print("\n4. URL validation patterns:\n", .{});

    const test_urls = [_][]const u8{
        "https://valid.example.com/path",
        "http://localhost:8080",
        "https://user:pass@secure.example.com/api",
        "ftp://files.example.com/downloads",
        "wss://websocket.example.com/socket",
    };

    for (test_urls) |test_url| {
        var validated = try url.Url.parse(allocator, test_url);
        defer validated.deinit();
        std.debug.print("   {s}\n", .{test_url});
        std.debug.print("      Default port: {}, Secure: {}\n", .{ validated.defaultPort(), validated.isSecure() });
    }

    // Example 5: Dynamic URL building
    std.debug.print("\n5. Dynamic URL building:\n", .{});

    var api_builder = url.UrlBuilder.init(allocator);
    defer api_builder.deinit();

    // Simulate building an API URL with multiple parameters
    try api_builder.setScheme("https");
    try api_builder.setHost("api.example.com");
    try api_builder.setPath("/v2/search");

    // Add multiple query parameters dynamically
    const search_params = .{
        .query = "zig programming language",
        .limit = "20",
        .offset = "0",
        .sort = "relevance",
        .order = "desc",
    };

    inline for (@typeInfo(@TypeOf(search_params)).Struct.fields) |field| {
        const value = @field(search_params, field.name);
        const encoded_key = try url.percentEncode(allocator, field.name);
        defer allocator.free(encoded_key);
        const encoded_value = try url.percentEncode(allocator, value);
        defer allocator.free(encoded_value);
        try api_builder.addQueryParam(encoded_key, encoded_value);
    }

    const api_url = try api_builder.build();
    defer allocator.free(api_url);
    std.debug.print("   API URL: {s}\n\n", .{api_url});

    // Example 6: Error handling
    std.debug.print("6. Error handling:\n", .{});

    const invalid_urls = [_][]const u8{
        "not-a-url",
        "://missing-scheme.com",
        "http://",
    };

    for (invalid_urls) |invalid_url| {
        const result = url.Url.parse(allocator, invalid_url);
        if (result) |_| {
            std.debug.print("   '{s}' - Unexpected success\n", .{invalid_url});
        } else |err| {
            std.debug.print("   '{s}' - Error: {}\n", .{ invalid_url, err });
        }
    }

    // Example 7: Batch URL processing
    std.debug.print("\n7. Batch URL processing:\n", .{});

    const urls_to_process = [_][]const u8{
        "https://api.example.com/users/1",
        "https://api.example.com/users/2",
        "https://api.example.com/users/3",
        "https://api.example.com/posts?author=1",
    };

    for (urls_to_process) |u| {
        var batch_parsed = try url.Url.parse(allocator, u);
        defer batch_parsed.deinit();

        std.debug.print("   {s}\n", .{u});
        std.debug.print("      Host: {s}, Path: {s}\n", .{ batch_parsed.host, batch_parsed.path });

        if (batch_parsed.query.len > 0) {
            var params = try batch_parsed.getQueryParams(allocator);
            defer {
                var iter = params.iterator();
                while (iter.next()) |entry| {
                    allocator.free(entry.key_ptr.*);
                    allocator.free(entry.value_ptr.*);
                }
                params.deinit();
            }
            std.debug.print("      Query params: {} items\n", .{params.count()});
        }
    }

    // Example 8: URL construction for different schemes
    std.debug.print("\n8. Different schemes and default ports:\n", .{});

    const schemes = [_]struct { scheme: []const u8, host: []const u8 }{
        .{ .scheme = "http", .host = "example.com" },
        .{ .scheme = "https", .host = "example.com" },
        .{ .scheme = "ws", .host = "websocket.example.com" },
        .{ .scheme = "wss", .host = "websocket.example.com" },
        .{ .scheme = "ftp", .host = "ftp.example.com" },
    };

    for (schemes) |s| {
        var scheme_builder = url.UrlBuilder.init(allocator);
        defer scheme_builder.deinit();

        try scheme_builder.setScheme(s.scheme);
        try scheme_builder.setHost(s.host);
        try scheme_builder.setPath("/");

        var parsed_scheme = try url.Url.parse(allocator, try scheme_builder.build());
        defer parsed_scheme.deinit();
        allocator.free(parsed_scheme.toString(allocator) catch unreachable);

        std.debug.print("   {s}: default port = {}\n", .{ s.scheme, parsed_scheme.defaultPort() });
    }
}