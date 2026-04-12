// Example: Basic JSON parsing and querying
// Run: zig run example_basic.zig

const std = @import("std");

// Import from main module
const JsonParser = @import("src/main.zig").JsonParser;
const JsonQuery = @import("src/main.zig").JsonQuery;
const JsonValue = @import("src/main.zig").JsonValue;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const stdout = std.io.getStdOut().writer();

    // Example 1: Parse a simple object
    try stdout.print("=== Example 1: Simple Object ===\n", .{});
    const simple_json = "{\"name\": \"Alice\", \"age\": 30, \"active\": true}";
    var parser1 = JsonParser.init(allocator, simple_json);
    var obj1 = try parser1.parse();
    defer obj1.deinit(allocator);

    try stdout.print("Parsed: {}\n", .{obj1});
    try stdout.print("Name: {s}\n", .{obj1.get("name").?.asString().?});
    try stdout.print("Age: {}\n", .{obj1.get("age").?.asInt().?});
    try stdout.print("Active: {}\n\n", .{obj1.get("active").?.asBool().?});

    // Example 2: Parse an array
    try stdout.print("=== Example 2: Array ===\n", .{});
    const array_json = "[1, 2, 3, 4, 5]";
    var parser2 = JsonParser.init(allocator, array_json);
    var arr = try parser2.parse();
    defer arr.deinit(allocator);

    const items = arr.asArray().?;
    try stdout.print("Array length: {}\n", .{items.len});
    try stdout.print("First item: {}\n", .{items[0].asInt().?});
    try stdout.print("Last item: {}\n\n", .{items[items.len - 1].asInt().?});

    // Example 3: Nested structures
    try stdout.print("=== Example 3: Nested Structures ===\n", .{});
    const nested_json =
        \\{
        \\  "company": "TechCorp",
        \\  "employees": [
        \\    {"name": "Alice", "department": "Engineering", "salary": 100000},
        \\    {"name": "Bob", "department": "Sales", "salary": 80000},
        \\    {"name": "Charlie", "department": "Engineering", "salary": 95000}
        \\  ],
        \\  "founded": 2010
        \\}
    ;
    var parser3 = JsonParser.init(allocator, nested_json);
    var company = try parser3.parse();
    defer company.deinit(allocator);

    try stdout.print("Company: {s}\n", .{company.get("company").?.asString().?});
    try stdout.print("Founded: {}\n", .{company.get("founded").?.asInt().?});

    const employees = company.get("employees").?.asArray().?;
    try stdout.print("Employees:\n", .{});
    for (employees, 0..) |emp, i| {
        try stdout.print(
            "  {}. {} - {} (${d})\n",
            .{
                i + 1,
                emp.get("name").?.asString().?,
                emp.get("department").?.asString().?,
                emp.get("salary").?.asInt().?,
            },
        );
    }
    try stdout.print("\n", .{});

    // Example 4: Using JsonQuery
    try stdout.print("=== Example 4: JsonQuery ===\n", .{});
    var query = JsonQuery.init(allocator);

    // Query nested path
    const first_emp_name = try query.query(company, "$.employees[0].name");
    try stdout.print("First employee name: {s}\n", .{first_emp_name.?.asString().?});

    // Query specific salary
    const second_salary = try query.query(company, "$.employees[1].salary");
    try stdout.print("Second employee salary: {}\n", .{second_salary.?.asInt().?});

    // Example 5: Deep key search
    try stdout.print("\n=== Example 5: Deep Key Search ===\n", .{});
    const deep_json =
        \\{
        \\  "user": {
        \\    "name": "Alice",
        \\    "profile": {
        \\      "name": "Alice Profile",
        \\      "settings": {
        \\        "name": "default"
        \\      }
        \\    }
        \\  },
        \\  "name": "Root Name"
        \\}
    ;
    var parser5 = JsonParser.init(allocator, deep_json);
    var deep_root = try parser5.parse();
    defer deep_root.deinit(allocator);

    var all_names = try query.findKey(deep_root, "name");
    defer all_names.deinit(allocator);

    try stdout.print("All 'name' values found:\n", .{});
    const names_array = all_names.asArray().?;
    for (names_array, 0..) |name_val, i| {
        try stdout.print("  {}. {s}\n", .{ i + 1, name_val.asString().? });
    }
}