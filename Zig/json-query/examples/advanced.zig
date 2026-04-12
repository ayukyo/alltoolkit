// Example: Advanced JSON query operations
// Run: zig run example_advanced.zig

const std = @import("std");

const JsonParser = @import("src/main.zig").JsonParser;
const JsonQuery = @import("src/main.zig").JsonQuery;
const JsonValue = @import("src/main.zig").JsonValue;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const stdout = std.io.getStdOut().writer();

    // Example: Processing API response
    try stdout.print("=== API Response Processing ===\n\n", .{});

    const api_response =
        \\{
        \\  "status": "success",
        \\  "data": {
        \\    "users": [
        \\      {
        \\        "id": 1,
        \\        "username": "alice",
        \\        "email": "alice@example.com",
        \\        "profile": {
        \\          "avatar": "avatar1.png",
        \\          "bio": "Software Engineer"
        \\        },
        \\        "roles": ["admin", "user"]
        \\      },
        \\      {
        \\        "id": 2,
        \\        "username": "bob",
        \\        "email": "bob@example.com",
        \\        "profile": {
        \\          "avatar": "avatar2.png",
        \\          "bio": "Designer"
        \\        },
        \\        "roles": ["user"]
        \\      },
        \\      {
        \\        "id": 3,
        \\        "username": "charlie",
        \\        "email": "charlie@example.com",
        \\        "profile": {
        \\          "avatar": "avatar3.png",
        \\          "bio": "DevOps Engineer"
        \\        },
        \\        "roles": ["admin", "user", "moderator"]
        \\      }
        \\    ],
        \\    "pagination": {
        \\      "page": 1,
        \\      "per_page": 10,
        \\      "total": 3
        \\    }
        \\  },
        \\  "meta": {
        \\    "request_id": "abc123",
        \\    "timestamp": 1699999999
        \\  }
        \\}
    ;

    var parser = JsonParser.init(allocator, api_response);
    var root = try parser.parse();
    defer root.deinit(allocator);

    var query = JsonQuery.init(allocator);

    // Extract status
    try stdout.print("Status: {s}\n", .{(try query.query(root, "$.status")).?.asString().?});

    // Get pagination info
    const total = try query.query(root, "$.data.pagination.total");
    try stdout.print("Total users: {}\n\n", .{total.?.asInt().?});

    // Process each user
    try stdout.print("Users:\n", .{});
    const users = (try query.query(root, "$.data.users")).?.asArray().?;

    for (users, 0..) |user, i| {
        const username = user.get("username").?.asString().?;
        const email = user.get("email").?.asString().?;
        const bio = (try query.query(user, "$.profile.bio")).?.asString().?;
        const roles = user.get("roles").?.asArray().?;

        try stdout.print("{}. @{s}\n", .{ i + 1, username });
        try stdout.print("   Email: {s}\n", .{email});
        try stdout.print("   Bio: {s}\n", .{bio});
        try stdout.print("   Roles: ", .{});
        for (roles, 0..) |role, j| {
            if (j > 0) try stdout.print(", ", .{});
            try stdout.print("{s}", .{role.asString().?});
        }
        try stdout.print("\n\n", .{});
    }

    // Deep search for all IDs
    try stdout.print("=== Deep Search: All IDs ===\n", .{});
    var all_ids = try query.findKey(root, "id");
    defer all_ids.deinit(allocator);

    const ids = all_ids.asArray().?;
    try stdout.print("Found {} ID(s): ", .{ids.len});
    for (ids, 0..) |id, i| {
        if (i > 0) try stdout.print(", ", .{});
        try stdout.print("{}", .{id.asInt().?});
    }
    try stdout.print("\n\n", .{});

    // Find all emails
    try stdout.print("=== Deep Search: All Emails ===\n", .{});
    var all_emails = try query.findKey(root, "email");
    defer all_emails.deinit(allocator);

    const emails = all_emails.asArray().?;
    try stdout.print("Found {} email(s):\n", .{emails.len});
    for (emails) |email| {
        try stdout.print("  - {s}\n", .{email.asString().?});
    }
    try stdout.print("\n", .{});

    // Demonstrate type checking
    try stdout.print("=== Type Information ===\n", .{});
    const status_type = (try query.query(root, "$.status")).?.getType();
    const users_type = (try query.query(root, "$.data.users")).?.getType();
    const page_type = (try query.query(root, "$.data.pagination.page")).?.getType();

    try stdout.print("status type: {s}\n", .{status_type});
    try stdout.print("users type: {s}\n", .{users_type});
    try stdout.print("page type: {s}\n", .{page_type});
}