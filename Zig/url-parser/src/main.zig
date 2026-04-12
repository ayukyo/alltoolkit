const std = @import("std");

/// URL parsing errors
pub const UrlError = error{
    InvalidUrl,
    InvalidScheme,
    InvalidPort,
    InvalidHost,
    InvalidPercentEncoding,
    OutOfMemory,
};

/// URL components
pub const Url = struct {
    scheme: []const u8,
    host: []const u8,
    port: ?u16,
    path: []const u8,
    query: []const u8,
    fragment: []const u8,
    username: []const u8,
    password: []const u8,
    allocator: std.mem.Allocator,

    const Self = @This();

    /// Parse a URL string into components
    pub fn parse(allocator: std.mem.Allocator, url_str: []const u8) UrlError!Self {
        var self = Self{
            .scheme = &.{},
            .host = &.{},
            .port = null,
            .path = &.{},
            .query = &.{},
            .fragment = &.{},
            .username = &.{},
            .password = &.{},
            .allocator = allocator,
        };

        var remaining = url_str;

        // Parse scheme
        if (std.mem.indexOf(u8, remaining, "://")) |scheme_end| {
            if (scheme_end == 0) return UrlError.InvalidScheme; // Empty scheme
            self.scheme = try allocator.dupe(u8, remaining[0..scheme_end]);
            remaining = remaining[scheme_end + 3 ..];
        } else {
            return UrlError.InvalidScheme;
        }

        // Parse fragment
        if (std.mem.indexOf(u8, remaining, "#")) |frag_start| {
            self.fragment = try allocator.dupe(u8, remaining[frag_start + 1 ..]);
            remaining = remaining[0..frag_start];
        }

        // Parse query
        if (std.mem.indexOf(u8, remaining, "?")) |query_start| {
            self.query = try allocator.dupe(u8, remaining[query_start + 1 ..]);
            remaining = remaining[0..query_start];
        }

        // Parse path (find first / after authority)
        var authority_end = remaining.len;
        if (std.mem.indexOf(u8, remaining, "/")) |path_start| {
            authority_end = path_start;
            self.path = try allocator.dupe(u8, remaining[path_start..]);
        } else {
            self.path = try allocator.dupe(u8, "/");
        }

        // Parse authority (user:pass@host:port)
        const authority = remaining[0..authority_end];

        // Find @ for credentials
        var host_port = authority;
        if (std.mem.indexOf(u8, authority, "@")) |at_pos| {
            const credentials = authority[0..at_pos];
            host_port = authority[at_pos + 1 ..];

            // Parse username:password
            if (std.mem.indexOf(u8, credentials, ":")) |colon_pos| {
                self.username = try allocator.dupe(u8, credentials[0..colon_pos]);
                self.password = try allocator.dupe(u8, credentials[colon_pos + 1 ..]);
            } else {
                self.username = try allocator.dupe(u8, credentials);
            }
        }

        // Parse host:port
        if (std.mem.startsWith(u8, host_port, "[")) {
            // IPv6 address
            if (std.mem.indexOf(u8, host_port, "]")) |bracket_end| {
                self.host = try allocator.dupe(u8, host_port[0 .. bracket_end + 1]);
                const after_bracket = host_port[bracket_end + 1 ..];
                if (std.mem.startsWith(u8, after_bracket, ":")) {
                    const port_str = after_bracket[1..];
                    self.port = try parsePort(port_str);
                }
            } else {
                return UrlError.InvalidHost;
            }
        } else if (std.mem.indexOf(u8, host_port, ":")) |colon_pos| {
            self.host = try allocator.dupe(u8, host_port[0..colon_pos]);
            const port_str = host_port[colon_pos + 1 ..];
            self.port = try parsePort(port_str);
        } else if (host_port.len > 0) {
            self.host = try allocator.dupe(u8, host_port);
        }

        return self;
    }

    /// Free all allocated memory
    pub fn deinit(self: *Self) void {
        self.allocator.free(self.scheme);
        if (self.host.len > 0) self.allocator.free(self.host);
        if (self.path.len > 0) self.allocator.free(self.path);
        if (self.query.len > 0) self.allocator.free(self.query);
        if (self.fragment.len > 0) self.allocator.free(self.fragment);
        if (self.username.len > 0) self.allocator.free(self.username);
        if (self.password.len > 0) self.allocator.free(self.password);
    }

    /// Reconstruct URL string
    pub fn toString(self: Self, allocator: std.mem.Allocator) ![]const u8 {
        var result = std.ArrayList(u8).init(allocator);
        defer result.deinit();
        const writer = result.writer();

        try writer.writeAll(self.scheme);
        try writer.writeAll("://");

        if (self.username.len > 0) {
            try writer.writeAll(self.username);
            if (self.password.len > 0) {
                try writer.writeAll(":");
                try writer.writeAll(self.password);
            }
            try writer.writeAll("@");
        }

        try writer.writeAll(self.host);

        if (self.port) |p| {
            try writer.print(":{}", .{p});
        }

        try writer.writeAll(self.path);

        if (self.query.len > 0) {
            try writer.writeAll("?");
            try writer.writeAll(self.query);
        }

        if (self.fragment.len > 0) {
            try writer.writeAll("#");
            try writer.writeAll(self.fragment);
        }

        return result.toOwnedSlice();
    }

    /// Get default port for scheme
    pub fn defaultPort(self: Self) u16 {
        if (self.port) |p| return p;

        if (std.ascii.eqlIgnoreCase(self.scheme, "http")) return 80;
        if (std.ascii.eqlIgnoreCase(self.scheme, "https")) return 443;
        if (std.ascii.eqlIgnoreCase(self.scheme, "ftp")) return 21;
        if (std.ascii.eqlIgnoreCase(self.scheme, "ssh")) return 22;
        if (std.ascii.eqlIgnoreCase(self.scheme, "telnet")) return 23;
        if (std.ascii.eqlIgnoreCase(self.scheme, "smtp")) return 25;
        if (std.ascii.eqlIgnoreCase(self.scheme, "dns")) return 53;
        if (std.ascii.eqlIgnoreCase(self.scheme, "ws")) return 80;
        if (std.ascii.eqlIgnoreCase(self.scheme, "wss")) return 443;

        return 0;
    }

    /// Check if URL uses secure scheme
    pub fn isSecure(self: Self) bool {
        return std.ascii.eqlIgnoreCase(self.scheme, "https") or
            std.ascii.eqlIgnoreCase(self.scheme, "wss");
    }

    /// Get query parameters as key-value pairs
    pub fn getQueryParams(self: Self, allocator: std.mem.Allocator) !std.StringHashMap([]const u8) {
        var params = std.StringHashMap([]const u8).init(allocator);
        errdefer params.deinit();

        if (self.query.len == 0) return params;

        var iter = std.mem.splitSequence(u8, self.query, "&");
        while (iter.next()) |param| {
            if (std.mem.indexOf(u8, param, "=")) |eq_pos| {
                const key = param[0..eq_pos];
                const value = param[eq_pos + 1 ..];
                const key_dup = try allocator.dupe(u8, key);
                const value_dup = try allocator.dupe(u8, value);
                try params.put(key_dup, value_dup);
            } else {
                const key_dup = try allocator.dupe(u8, param);
                const value_dup = try allocator.dupe(u8, "");
                try params.put(key_dup, value_dup);
            }
        }

        return params;
    }

    /// Format for debugging
    pub fn format(
        self: Self,
        comptime fmt: []const u8,
        options: std.fmt.FormatOptions,
        writer: anytype,
    ) !void {
        _ = fmt;
        _ = options;
        try writer.print("URL{{ scheme: {s}, host: {s}, port: {any}, path: {s}, query: {s}, fragment: {s} }}", .{
            self.scheme,
            self.host,
            self.port,
            self.path,
            self.query,
            self.fragment,
        });
    }
};

/// Parse port string to u16
fn parsePort(port_str: []const u8) UrlError!u16 {
    if (port_str.len == 0) return UrlError.InvalidPort;
    var result: u32 = 0;
    for (port_str) |c| {
        if (c < '0' or c > '9') return UrlError.InvalidPort;
        result = result * 10 + (c - '0');
        if (result > 65535) return UrlError.InvalidPort;
        }
    return @intCast(result);
}

/// URL Builder for constructing URLs
pub const UrlBuilder = struct {
    scheme: []const u8,
    scheme_allocated: bool,
    host: []const u8,
    host_allocated: bool,
    port: ?u16,
    path: []const u8,
    path_allocated: bool,
    query_params: std.StringHashMap([]const u8),
    fragment: ?[]const u8,
    username: ?[]const u8,
    password: ?[]const u8,
    allocator: std.mem.Allocator,

    const Self = @This();

    /// Initialize a new URL builder
    pub fn init(allocator: std.mem.Allocator) Self {
        return .{
            .scheme = "https",
            .scheme_allocated = false,
            .host = "",
            .host_allocated = false,
            .port = null,
            .path = "/",
            .path_allocated = false,
            .query_params = std.StringHashMap([]const u8).init(allocator),
            .fragment = null,
            .username = null,
            .password = null,
            .allocator = allocator,
        };
    }

    /// Free all allocated memory
    pub fn deinit(self: *Self) void {
        if (self.scheme_allocated) self.allocator.free(self.scheme);
        if (self.host_allocated) self.allocator.free(self.host);
        if (self.path_allocated) self.allocator.free(self.path);
        var iter = self.query_params.iterator();
        while (iter.next()) |entry| {
            self.allocator.free(entry.key_ptr.*);
            self.allocator.free(entry.value_ptr.*);
        }
        self.query_params.deinit();
        if (self.fragment) |f| self.allocator.free(f);
        if (self.username) |u| self.allocator.free(u);
        if (self.password) |p| self.allocator.free(p);
    }

    /// Set the scheme (http, https, etc.)
    pub fn setScheme(self: *Self, scheme: []const u8) !void {
        if (self.scheme_allocated) self.allocator.free(self.scheme);
        self.scheme = try self.allocator.dupe(u8, scheme);
        self.scheme_allocated = true;
    }

    /// Set the host
    pub fn setHost(self: *Self, host: []const u8) !void {
        if (self.host_allocated) self.allocator.free(self.host);
        self.host = try self.allocator.dupe(u8, host);
        self.host_allocated = true;
    }

    /// Set the port
    pub fn setPort(self: *Self, port: u16) void {
        self.port = port;
    }

    /// Set the path
    pub fn setPath(self: *Self, path: []const u8) !void {
        if (self.path_allocated) self.allocator.free(self.path);
        self.path = try self.allocator.dupe(u8, path);
        self.path_allocated = true;
    }

    /// Add a query parameter
    pub fn addQueryParam(self: *Self, key: []const u8, value: []const u8) !void {
        const value_dup = try self.allocator.dupe(u8, value);
        
        // Check if key already exists
        if (self.query_params.getPtr(key)) |old_value_ptr| {
            // Key exists: free old value, update with new value
            self.allocator.free(old_value_ptr.*);
            // Use getOrPut to update the existing entry
            const gop = try self.query_params.getOrPut(key);
            // The key_ptr is already set (existing), just update value
            gop.value_ptr.* = value_dup;
        } else {
            // Key doesn't exist: allocate key and add new entry
            const key_dup = try self.allocator.dupe(u8, key);
            try self.query_params.put(key_dup, value_dup);
        }
    }

    /// Set the fragment
    pub fn setFragment(self: *Self, fragment: []const u8) !void {
        if (self.fragment) |f| self.allocator.free(f);
        self.fragment = try self.allocator.dupe(u8, fragment);
    }

    /// Set credentials
    pub fn setCredentials(self: *Self, username: []const u8, password: []const u8) !void {
        if (self.username) |u| self.allocator.free(u);
        if (self.password) |p| self.allocator.free(p);
        self.username = try self.allocator.dupe(u8, username);
        self.password = try self.allocator.dupe(u8, password);
    }

    /// Build the URL string
    pub fn build(self: *Self) ![]const u8 {
        var result = std.ArrayList(u8).init(self.allocator);
        defer result.deinit();
        const writer = result.writer();

        try writer.writeAll(self.scheme);
        try writer.writeAll("://");

        if (self.username) |u| {
            try writer.writeAll(u);
            if (self.password) |p| {
                try writer.writeAll(":");
                try writer.writeAll(p);
            }
            try writer.writeAll("@");
        }

        try writer.writeAll(self.host);

        if (self.port) |p| {
            try writer.print(":{}", .{p});
        }

        try writer.writeAll(self.path);

        if (self.query_params.count() > 0) {
            try writer.writeAll("?");
            var first = true;
            var iter = self.query_params.iterator();
            while (iter.next()) |entry| {
                if (!first) try writer.writeAll("&");
                first = false;
                try writer.writeAll(entry.key_ptr.*);
                try writer.writeAll("=");
                try writer.writeAll(entry.value_ptr.*);
            }
        }

        if (self.fragment) |f| {
            try writer.writeAll("#");
            try writer.writeAll(f);
        }

        return result.toOwnedSlice();
    }
};

/// Percent-encode a string for URLs
pub fn percentEncode(allocator: std.mem.Allocator, input: []const u8) ![]const u8 {
    var result = std.ArrayList(u8).init(allocator);
    defer result.deinit();

    const hex_chars = "0123456789ABCDEF";

    for (input) |c| {
        if (isUnreserved(c)) {
            try result.append(c);
        } else {
            try result.append('%');
            try result.append(hex_chars[(c >> 4) & 0x0F]);
            try result.append(hex_chars[c & 0x0F]);
        }
    }

    return result.toOwnedSlice();
}

/// Percent-decode a string
pub fn percentDecode(allocator: std.mem.Allocator, input: []const u8) UrlError![]const u8 {
    var result = std.ArrayList(u8).init(allocator);
    defer result.deinit();

    var i: usize = 0;
    while (i < input.len) {
        if (input[i] == '%') {
            if (i + 2 >= input.len) return UrlError.InvalidPercentEncoding;
            const hex = input[i + 1 .. i + 3];
            const byte = std.fmt.parseInt(u8, hex, 16) catch
                return UrlError.InvalidPercentEncoding;
            try result.append(byte);
            i += 3;
        } else if (input[i] == '+') {
            try result.append(' ');
            i += 1;
        } else {
            try result.append(input[i]);
            i += 1;
        }
    }

    return result.toOwnedSlice();
}

/// Check if character is unreserved (doesn't need encoding)
fn isUnreserved(c: u8) bool {
    return (c >= 'A' and c <= 'Z') or
        (c >= 'a' and c <= 'z') or
        (c >= '0' and c <= '9') or
        c == '-' or c == '.' or c == '_' or c == '~';
}

/// Join path segments
pub fn joinPath(allocator: std.mem.Allocator, segments: []const []const u8) ![]const u8 {
    var result = std.ArrayList(u8).init(allocator);
    defer result.deinit();

    for (segments, 0..) |segment, i| {
        if (i > 0 and result.items.len > 0 and result.items[result.items.len - 1] != '/') {
            try result.append('/');
        }
        if (std.mem.startsWith(u8, segment, "/") and result.items.len > 0) {
            try result.appendSlice(segment[1..]);
        } else {
            try result.appendSlice(segment);
        }
    }

    return result.toOwnedSlice();
}

/// Extract file extension from path
pub fn getExtension(path: []const u8) ?[]const u8 {
    const filename = std.mem.lastIndexOf(u8, path, "/") orelse 0;
    const basename = path[filename + 1 ..];
    if (std.mem.lastIndexOf(u8, basename, ".")) |dot_pos| {
        if (dot_pos > 0 and dot_pos < basename.len - 1) {
            return basename[dot_pos + 1 ..];
        }
    }
    return null;
}

/// Extract filename from path
pub fn getFilename(path: []const u8) []const u8 {
    if (std.mem.lastIndexOf(u8, path, "/")) |slash_pos| {
        return path[slash_pos + 1 ..];
    }
    return path;
}

// ============================================================================
// Tests
// ============================================================================

test "Url.parse - basic URL" {
    const allocator = std.testing.allocator;

    var url = try Url.parse(allocator, "https://example.com/path?query=value#fragment");
    defer url.deinit();

    try std.testing.expectEqualStrings("https", url.scheme);
    try std.testing.expectEqualStrings("example.com", url.host);
    try std.testing.expectEqual(@as(?u16, null), url.port);
    try std.testing.expectEqualStrings("/path", url.path);
    try std.testing.expectEqualStrings("query=value", url.query);
    try std.testing.expectEqualStrings("fragment", url.fragment);
}

test "Url.parse - with port" {
    const allocator = std.testing.allocator;

    var url = try Url.parse(allocator, "http://localhost:8080/api");
    defer url.deinit();

    try std.testing.expectEqualStrings("http", url.scheme);
    try std.testing.expectEqualStrings("localhost", url.host);
    try std.testing.expectEqual(@as(?u16, 8080), url.port);
    try std.testing.expectEqualStrings("/api", url.path);
}

test "Url.parse - with credentials" {
    const allocator = std.testing.allocator;

    var url = try Url.parse(allocator, "https://user:pass@example.com/resource");
    defer url.deinit();

    try std.testing.expectEqualStrings("user", url.username);
    try std.testing.expectEqualStrings("pass", url.password);
    try std.testing.expectEqualStrings("example.com", url.host);
}

test "Url.parse - IPv6 host" {
    const allocator = std.testing.allocator;

    var url = try Url.parse(allocator, "http://[::1]:3000/test");
    defer url.deinit();

    try std.testing.expectEqualStrings("[::1]", url.host);
    try std.testing.expectEqual(@as(?u16, 3000), url.port);
}

test "Url.parse - no path" {
    const allocator = std.testing.allocator;

    var url = try Url.parse(allocator, "https://example.com");
    defer url.deinit();

    try std.testing.expectEqualStrings("/", url.path);
}

test "Url.toString - reconstruct URL" {
    const allocator = std.testing.allocator;

    var url = try Url.parse(allocator, "https://example.com/path?key=value#section");
    defer url.deinit();

    const result = try url.toString(allocator);
    defer allocator.free(result);

    try std.testing.expectEqualStrings("https://example.com/path?key=value#section", result);
}

test "Url.defaultPort - known schemes" {
    const allocator = std.testing.allocator;

    var http_url = try Url.parse(allocator, "http://example.com");
    defer http_url.deinit();
    try std.testing.expectEqual(@as(u16, 80), http_url.defaultPort());

    var https_url = try Url.parse(allocator, "https://example.com");
    defer https_url.deinit();
    try std.testing.expectEqual(@as(u16, 443), https_url.defaultPort());
}

test "Url.isSecure" {
    const allocator = std.testing.allocator;

    var https_url = try Url.parse(allocator, "https://example.com");
    defer https_url.deinit();
    try std.testing.expect(https_url.isSecure());

    var http_url = try Url.parse(allocator, "http://example.com");
    defer http_url.deinit();
    try std.testing.expect(!http_url.isSecure());
}

test "Url.getQueryParams" {
    const allocator = std.testing.allocator;

    var url = try Url.parse(allocator, "https://example.com?key1=value1&key2=value2&key3");
    defer url.deinit();

    var params = try url.getQueryParams(allocator);
    defer {
        var iter = params.iterator();
        while (iter.next()) |entry| {
            allocator.free(entry.key_ptr.*);
            allocator.free(entry.value_ptr.*);
        }
        params.deinit();
    }

    try std.testing.expectEqual(@as(usize, 3), params.count());
    try std.testing.expectEqualStrings("value1", params.get("key1").?);
    try std.testing.expectEqualStrings("value2", params.get("key2").?);
}

test "UrlBuilder - build URL" {
    const allocator = std.testing.allocator;

    var builder = UrlBuilder.init(allocator);
    defer builder.deinit();

    try builder.setHost("api.example.com");
    try builder.setPath("/v1/users");
    try builder.addQueryParam("page", "1");
    try builder.addQueryParam("limit", "10");
    try builder.setFragment("results");

    const result = try builder.build();
    defer allocator.free(result);

    // Check components are present (order may vary for query params)
    try std.testing.expect(std.mem.startsWith(u8, result, "https://api.example.com/v1/users?"));
    try std.testing.expect(std.mem.indexOf(u8, result, "page=1") != null);
    try std.testing.expect(std.mem.indexOf(u8, result, "limit=10") != null);
    try std.testing.expect(std.mem.endsWith(u8, result, "#results"));
}

test "UrlBuilder - with credentials and port" {
    const allocator = std.testing.allocator;

    var builder = UrlBuilder.init(allocator);
    defer builder.deinit();

    try builder.setScheme("http");
    try builder.setHost("localhost");
    builder.setPort(8080);
    try builder.setCredentials("admin", "secret");
    try builder.setPath("/api");

    const result = try builder.build();
    defer allocator.free(result);

    try std.testing.expectEqualStrings("http://admin:secret@localhost:8080/api", result);
}

test "percentEncode - encode special characters" {
    const allocator = std.testing.allocator;

    const encoded = try percentEncode(allocator, "hello world!");
    defer allocator.free(encoded);

    try std.testing.expectEqualStrings("hello%20world%21", encoded);
}

test "percentDecode - decode encoded string" {
    const allocator = std.testing.allocator;

    const decoded = try percentDecode(allocator, "hello%20world%21");
    defer allocator.free(decoded);

    try std.testing.expectEqualStrings("hello world!", decoded);
}

test "percentDecode - plus to space" {
    const allocator = std.testing.allocator;

    const decoded = try percentDecode(allocator, "hello+world");
    defer allocator.free(decoded);

    try std.testing.expectEqualStrings("hello world", decoded);
}

test "joinPath - join segments" {
    const allocator = std.testing.allocator;

    const segments = [_][]const u8{ "api", "/v1/", "users", "/list" };
    const path = try joinPath(allocator, &segments);
    defer allocator.free(path);

    try std.testing.expectEqualStrings("api/v1/users/list", path);
}

test "getExtension - extract extension" {
    try std.testing.expectEqualStrings("txt", getExtension("/path/to/file.txt").?);
    try std.testing.expectEqualStrings("json", getExtension("data.json").?);
    try std.testing.expectEqualStrings("html", getExtension("/index.html").?);
    try std.testing.expectEqual(null, getExtension("/noextension"));
    try std.testing.expectEqual(null, getExtension("/."));
}

test "getFilename - extract filename" {
    try std.testing.expectEqualStrings("file.txt", getFilename("/path/to/file.txt"));
    try std.testing.expectEqualStrings("data.json", getFilename("data.json"));
    try std.testing.expectEqualStrings("index.html", getFilename("/index.html"));
}

test "parsePort - valid ports" {
    try std.testing.expectEqual(@as(u16, 80), try parsePort("80"));
    try std.testing.expectEqual(@as(u16, 443), try parsePort("443"));
    try std.testing.expectEqual(@as(u16, 8080), try parsePort("8080"));
    try std.testing.expectEqual(@as(u16, 65535), try parsePort("65535"));
}

test "parsePort - invalid ports" {
    try std.testing.expectError(UrlError.InvalidPort, parsePort(""));
    try std.testing.expectError(UrlError.InvalidPort, parsePort("abc"));
    try std.testing.expectError(UrlError.InvalidPort, parsePort("65536"));
    try std.testing.expectError(UrlError.InvalidPort, parsePort("99999"));
}

test "Url.parse - error cases" {
    const allocator = std.testing.allocator;

    try std.testing.expectError(UrlError.InvalidScheme, Url.parse(allocator, "example.com"));
    try std.testing.expectError(UrlError.InvalidScheme, Url.parse(allocator, "://example.com"));
}

test "UrlBuilder - multiple query params with same key" {
    const allocator = std.testing.allocator;

    var builder = UrlBuilder.init(allocator);
    defer builder.deinit();

    try builder.setHost("example.com");
    try builder.addQueryParam("tag", "one");
    // Note: second call with same key will overwrite
    try builder.addQueryParam("tag", "two");

    const result = try builder.build();
    defer allocator.free(result);

    // Last value wins
    try std.testing.expect(std.mem.indexOf(u8, result, "tag=two") != null);
}

test "percentEncode - reserved characters" {
    const allocator = std.testing.allocator;

    const encoded = try percentEncode(allocator, "key=value&other=thing");
    defer allocator.free(encoded);

    // = and & should be encoded
    try std.testing.expect(std.mem.indexOf(u8, encoded, "=") == null);
    try std.testing.expect(std.mem.indexOf(u8, encoded, "&") == null);
}

test "percentDecode - round trip" {
    const allocator = std.testing.allocator;

    const original = "Hello World! @#$%";
    const encoded = try percentEncode(allocator, original);
    defer allocator.free(encoded);

    const decoded = try percentDecode(allocator, encoded);
    defer allocator.free(decoded);

    try std.testing.expectEqualStrings(original, decoded);
}