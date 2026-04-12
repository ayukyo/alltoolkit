const std = @import("std");
const url = @import("url");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== URL Parser - Basic Usage ===\n\n", .{});

    // Example 1: Parse a simple URL
    std.debug.print("1. Parse a simple URL:\n", .{});
    const simple_url = "https://example.com/path/to/resource";
    var parsed = try url.Url.parse(allocator, simple_url);
    defer parsed.deinit();

    std.debug.print("   Original: {s}\n", .{simple_url});
    std.debug.print("   Scheme: {s}\n", .{parsed.scheme});
    std.debug.print("   Host: {s}\n", .{parsed.host});
    std.debug.print("   Path: {s}\n", .{parsed.path});
    std.debug.print("   Default port: {}\n\n", .{parsed.defaultPort()});

    // Example 2: Parse URL with query and fragment
    std.debug.print("2. Parse URL with query and fragment:\n", .{});
    const complex_url = "https://api.example.com/v1/users?page=1&limit=10&sort=name#results";
    var complex_parsed = try url.Url.parse(allocator, complex_url);
    defer complex_parsed.deinit();

    std.debug.print("   Original: {s}\n", .{complex_url});
    std.debug.print("   Query: {s}\n", .{complex_parsed.query});
    std.debug.print("   Fragment: {s}\n", .{complex_parsed.fragment});

    // Get query parameters
    var query_params = try complex_parsed.getQueryParams(allocator);
    defer {
        var iter = query_params.iterator();
        while (iter.next()) |entry| {
            allocator.free(entry.key_ptr.*);
            allocator.free(entry.value_ptr.*);
        }
        query_params.deinit();
    }
    std.debug.print("   Page: {s}\n", .{query_params.get("page").?});
    std.debug.print("   Limit: {s}\n", .{query_params.get("limit").?});
    std.debug.print("   Sort: {s}\n\n", .{query_params.get("sort").?});

    // Example 3: Parse URL with port and credentials
    std.debug.print("3. Parse URL with credentials and port:\n", .{});
    const auth_url = "https://admin:secret123@private.example.com:8443/admin/dashboard";
    var auth_parsed = try url.Url.parse(allocator, auth_url);
    defer auth_parsed.deinit();

    std.debug.print("   Original: {s}\n", .{auth_url});
    std.debug.print("   Username: {s}\n", .{auth_parsed.username});
    std.debug.print("   Password: {s}\n", .{auth_parsed.password});
    std.debug.print("   Host: {s}\n", .{auth_parsed.host});
    std.debug.print("   Port: {}\n\n", .{auth_parsed.port.?});

    // Example 4: Build a URL from scratch
    std.debug.print("4. Build a URL:\n", .{});
    var builder = url.UrlBuilder.init(allocator);
    defer builder.deinit();

    try builder.setHost("api.example.com");
    try builder.setPath("/v1/search");
    try builder.addQueryParam("q", "ziglang");
    try builder.addQueryParam("page", "1");

    const built_url = try builder.build();
    defer allocator.free(built_url);

    std.debug.print("   Built URL: {s}\n\n", .{built_url});

    // Example 5: Percent encoding/decoding
    std.debug.print("5. Percent encoding/decoding:\n", .{});

    const text_to_encode = "hello world & goodbye!";
    const encoded = try url.percentEncode(allocator, text_to_encode);
    defer allocator.free(encoded);

    std.debug.print("   Original: {s}\n", .{text_to_encode});
    std.debug.print("   Encoded: {s}\n", .{encoded});

    const decoded = try url.percentDecode(allocator, encoded);
    defer allocator.free(decoded);

    std.debug.print("   Decoded: {s}\n\n", .{decoded});

    // Example 6: Path utilities
    std.debug.print("6. Path utilities:\n", .{});

    const path = "/documents/files/report.pdf";
    std.debug.print("   Path: {s}\n", .{path});
    std.debug.print("   Filename: {s}\n", .{url.getFilename(path)});
    std.debug.print("   Extension: {s}\n", .{url.getExtension(path).?});

    const segments = [_][]const u8{ "api", "v2", "users", "123" };
    const joined = try url.joinPath(allocator, &segments);
    defer allocator.free(joined);
    std.debug.print("   Joined path: {s}\n", .{joined});

    // Example 7: Security check
    std.debug.print("\n7. Security check:\n", .{});

    var secure_url = try url.Url.parse(allocator, "https://secure.example.com");
    defer secure_url.deinit();
    std.debug.print("   {s} - Secure: {}\n", .{ "https://secure.example.com", secure_url.isSecure() });

    var insecure_url = try url.Url.parse(allocator, "http://insecure.example.com");
    defer insecure_url.deinit();
    std.debug.print("   {s} - Secure: {}\n", .{ "http://insecure.example.com", insecure_url.isSecure() });
}