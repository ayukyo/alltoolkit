const std = @import("std");
const csv = @import("csv_utils");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    std.debug.print("=== CSV Utils Examples ===\n\n", .{});

    // Example 1: Basic CSV parsing
    std.debug.print("1. Basic CSV Parsing:\n", .{});
    const basic_csv = "name,age,city\nAlice,30,Beijing\nBob,25,Shanghai\nCharlie,35,Guangzhou";

    const records = csv.parseDefault(allocator, basic_csv) catch |err| {
        std.debug.print("Parse error: {}\n", .{err});
        return;
    };
    defer csv.freeRecords(allocator, records);

    std.debug.print("Parsed {} records:\n", .{records.len});
    for (records, 0..) |record, i| {
        std.debug.print("  Row {}: ", .{i});
        for (record.fields, 0..) |field, j| {
            if (j > 0) std.debug.print(", ", .{});
            std.debug.print("{s}", .{field});
        }
        std.debug.print("\n", .{});
    }

    // Example 2: Parse with type conversion
    std.debug.print("\n2. Type Conversion:\n", .{});
    std.debug.print("  Alice's age: {} (int)\n", .{records[1].asInt(1).?});
    std.debug.print("  Bob's age: {} (int)\n", .{records[2].asInt(1).?});

    // Example 3: CSV with quoted fields
    std.debug.print("\n3. Quoted Fields:\n", .{});
    const quoted_csv = "name,description\n\"Alice\",\"She said, \"\"Hello\"\"\"\n\"Bob\",\"A \"\"famous\"\" person\"";

    const quoted_records = csv.parseDefault(allocator, quoted_csv) catch |err| {
        std.debug.print("Parse error: {}\n", .{err});
        return;
    };
    defer csv.freeRecords(allocator, quoted_records);

    for (quoted_records, 0..) |record, i| {
        std.debug.print("  Row {}: name=\"{s}\", desc=\"{s}\"\n", .{ i, record.get(0).?, record.get(1).? });
    }

    // Example 4: Different delimiter
    std.debug.print("\n4. Different Delimiter (semicolon):\n", .{});
    const semicolon_csv = "name;age;score\nAlice;30;95.5\nBob;25;88.0";

    const semi_records = csv.parse(allocator, semicolon_csv, .{ .delimiter = ';' }) catch |err| {
        std.debug.print("Parse error: {}\n", .{err});
        return;
    };
    defer csv.freeRecords(allocator, semi_records);

    std.debug.print("  Scores: {} ({s}), {} ({s})\n", .{
        semi_records[1].asFloat(2).?,
        semi_records[1].get(0).?,
        semi_records[2].asFloat(2).?,
        semi_records[2].get(0).?,
    });

    // Example 5: CSV Writing
    std.debug.print("\n5. CSV Writing:\n", .{});
    const data_to_write = [_][]const []const u8{
        &[_][]const u8{ "product", "price", "quantity" },
        &[_][]const u8{ "Apple", "$1.50", "100" },
        &[_][]const u8{ "Banana", "$0.75", "200" },
        &[_][]const u8{ "Orange", "$2.00, each", "50" }, // Contains delimiter
    };

    var writer = csv.CsvWriter.init(allocator, .{});
    defer writer.deinit();

    for (data_to_write) |row| {
        writer.writeRecord(row) catch |err| {
            std.debug.print("Write error: {}\n", .{err});
            return;
        };
    }

    const output = writer.toOwnedSlice() catch |err| {
        std.debug.print("Output error: {}\n", .{err});
        return;
    };
    defer allocator.free(output);

    std.debug.print("Generated CSV:\n{s}\n", .{output});

    // Example 6: Count records without full parsing
    std.debug.print("\n6. Quick Record Count:\n", .{});
    const large_csv_preview = "a,b,c\n1,2,3\n4,5,6\n7,8,9\n10,11,12";
    const count = csv.countRecords(large_csv_preview, .{});
    std.debug.print("  Record count: {}\n", .{count});

    // Example 7: Parse with comments
    std.debug.print("\n7. CSV with Comments:\n", .{});
    const commented_csv = "# Employee data\nname,department,salary\n# Full-time employees\nAlice,Engineering,80000\nBob,Marketing,60000";

    const commented_records = csv.parse(allocator, commented_csv, .{ .comment = '#' }) catch |err| {
        std.debug.print("Parse error: {}\n", .{err});
        return;
    };
    defer csv.freeRecords(allocator, commented_records);

    std.debug.print("  Employee salaries:\n", .{});
    for (commented_records[1..]) |record| {
        std.debug.print("    {s}: {} ({s})\n", .{ record.get(0).?, record.asInt(2).?, record.get(1).? });
    }

    // Example 8: Parse with validation
    std.debug.print("\n8. Field Count Validation:\n", .{});
    const invalid_csv = "a,b,c\n1,2\n3,4,5"; // Row 1 has wrong count

    const valid_result = csv.parse(allocator, invalid_csv, .{ .expected_fields = 3 });
    if (valid_result) |_| {
        std.debug.print("  Unexpected success!\n", .{});
    } else |err| {
        std.debug.print("  Expected error: {} - validation working!\n", .{err});
    }

    // Example 9: Boolean parsing
    std.debug.print("\n9. Boolean Field Parsing:\n", .{});
    const bool_csv = "name,active,premium\nAlice,true,1\nBob,false,0\nCharlie,yes,no";

    const bool_records = csv.parseDefault(allocator, bool_csv) catch |err| {
        std.debug.print("Parse error: {}\n", .{err});
        return;
    };
    defer csv.freeRecords(allocator, bool_records);

    for (bool_records[1..]) |record| {
        std.debug.print("  {s}: active={?}, premium={?}\n", .{
            record.get(0).?,
            record.asBool(1),
            record.asBool(2),
        });
    }

    std.debug.print("\n=== All examples completed! ===\n", .{});
}