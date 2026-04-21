const std = @import("std");

/// CSV parsing and writing utilities for Zig
/// Zero external dependencies - pure standard library implementation

/// Errors that can occur during CSV operations
pub const CsvError = error{
    /// Memory allocation failed
    OutOfMemory,
    /// Invalid CSV format
    InvalidFormat,
    /// Quote not properly closed
    UnclosedQuote,
    /// Buffer too small for operation
    BufferTooSmall,
    /// Invalid escape sequence
    InvalidEscape,
    /// Field count mismatch
    FieldCountMismatch,
};

/// CSV parsing options
pub const ParseOptions = struct {
    /// Field delimiter (default: comma)
    delimiter: u8 = ',',
    /// Quote character (default: double quote)
    quote: u8 = '"',
    /// Escape character for quotes within quoted fields (default: double quote)
    escape: u8 = '"',
    /// Comment character (lines starting with this are skipped, 0 to disable)
    comment: u8 = 0,
    /// Trim leading whitespace from fields
    trim_leading: bool = false,
    /// Trim trailing whitespace from fields
    trim_trailing: bool = false,
    /// Skip empty lines
    skip_empty_lines: bool = true,
    /// Expected number of fields per record (0 for any)
    expected_fields: usize = 0,
};

/// CSV writing options
pub const WriteOptions = struct {
    /// Field delimiter (default: comma)
    delimiter: u8 = ',',
    /// Quote character (default: double quote)
    quote: u8 = '"',
    /// Always quote fields (even if not necessary)
    always_quote: bool = false,
    /// Quote fields containing the delimiter
    quote_delimiter: bool = true,
    /// Quote fields containing the quote character
    quote_quote: bool = true,
    /// Quote fields containing newlines
    quote_newline: bool = true,
    /// Include header row
    include_header: bool = true,
    /// Line ending
    line_ending: []const u8 = "\n",
};

/// Represents a single CSV record (row)
pub const CsvRecord = struct {
    fields: [][]u8,
    allocator: std.mem.Allocator,

    /// Initialize a new CsvRecord
    pub fn init(allocator: std.mem.Allocator, fields: [][]u8) CsvRecord {
        return .{
            .fields = fields,
            .allocator = allocator,
        };
    }

    /// Free the record's memory
    pub fn deinit(self: *CsvRecord) void {
        for (self.fields) |field| {
            self.allocator.free(field);
        }
        self.allocator.free(self.fields);
    }

    /// Get field at index
    pub fn get(self: CsvRecord, index: usize) ?[]const u8 {
        if (index >= self.fields.len) return null;
        return self.fields[index];
    }

    /// Get field count
    pub fn count(self: CsvRecord) usize {
        return self.fields.len;
    }

    /// Convert field to integer
    pub fn asInt(self: CsvRecord, index: usize) ?i64 {
        const field = self.get(index) orelse return null;
        return std.fmt.parseInt(i64, field, 10) catch null;
    }

    /// Convert field to float
    pub fn asFloat(self: CsvRecord, index: usize) ?f64 {
        const field = self.get(index) orelse return null;
        return std.fmt.parseFloat(f64, field) catch null;
    }

    /// Convert field to boolean
    pub fn asBool(self: CsvRecord, index: usize) ?bool {
        const field = self.get(index) orelse return null;
        const trimmed = std.mem.trim(u8, field, " \t");
        if (std.ascii.eqlIgnoreCase(trimmed, "true") or std.ascii.eqlIgnoreCase(trimmed, "1")) return true;
        if (std.ascii.eqlIgnoreCase(trimmed, "false") or std.ascii.eqlIgnoreCase(trimmed, "0")) return false;
        return null;
    }
};

/// CSV Parser - streaming parser for memory efficiency
pub const CsvParser = struct {
    allocator: std.mem.Allocator,
    options: ParseOptions,
    buffer: []u8,
    pos: usize,
    line: usize,

    /// Initialize a new CSV parser
    pub fn init(allocator: std.mem.Allocator, options: ParseOptions) CsvParser {
        return .{
            .allocator = allocator,
            .options = options,
            .buffer = &[_]u8{},
            .pos = 0,
            .line = 1,
        };
    }

    /// Parse a CSV string and return all records
    pub fn parseAll(self: *CsvParser, input: []const u8) CsvError![]CsvRecord {
        var records = std.ArrayList(CsvRecord).init(self.allocator);
        errdefer {
            for (records.items) |*rec| {
                rec.deinit();
            }
            records.deinit();
        }

        self.buffer = @constCast(input);
        self.pos = 0;
        self.line = 1;

        while (self.pos < self.buffer.len) {
            // Skip comment lines
            if (self.options.comment != 0 and self.pos < self.buffer.len and self.buffer[self.pos] == self.options.comment) {
                self.skipLine();
                continue;
            }

            // Skip empty lines
            if (self.options.skip_empty_lines) {
                const next_line_start = self.findNextLine();
                if (next_line_start == self.pos) {
                    self.skipLine();
                    continue;
                }
            }

            var record = try self.parseRecord();
            if (record.fields.len > 0) {
                try records.append(record);
            } else {
                record.deinit();
            }
        }

        return records.toOwnedSlice();
    }

    /// Parse a single record
    fn parseRecord(self: *CsvParser) CsvError!CsvRecord {
        var fields = std.ArrayList([]u8).init(self.allocator);
        errdefer {
            for (fields.items) |field| {
                self.allocator.free(field);
            }
            fields.deinit();
        }

        // Track whether we just consumed a delimiter (need trailing empty field)
        var after_delimiter = false;

        while (self.pos < self.buffer.len or after_delimiter) {
            after_delimiter = false;

            const field = try self.parseField();
            try fields.append(field);

            if (self.pos >= self.buffer.len) break;

            const ch = self.buffer[self.pos];
            if (ch == '\n' or ch == '\r') {
                self.skipNewline();
                break;
            } else if (ch == self.options.delimiter) {
                self.pos += 1;
                after_delimiter = true; // There might be another field (possibly empty)
            } else {
                // End of input or unexpected character
                break;
            }
        }

        // Validate field count if specified
        if (self.options.expected_fields > 0 and fields.items.len > 0 and fields.items.len != self.options.expected_fields) {
            return CsvError.FieldCountMismatch;
        }

        return CsvRecord.init(self.allocator, try fields.toOwnedSlice());
    }

    /// Parse a single field
    fn parseField(self: *CsvParser) CsvError![]u8 {
        self.skipWhitespace();

        if (self.pos >= self.buffer.len) {
            return self.allocator.dupe(u8, "") catch CsvError.OutOfMemory;
        }

        const ch = self.buffer[self.pos];

        // Quoted field
        if (ch == self.options.quote) {
            return self.parseQuotedField();
        }

        // Unquoted field
        return self.parseUnquotedField();
    }

    /// Parse a quoted field
    fn parseQuotedField(self: *CsvParser) CsvError![]u8 {
        self.pos += 1; // Skip opening quote

        var field = std.ArrayList(u8).init(self.allocator);
        defer field.deinit();

        while (self.pos < self.buffer.len) {
            const ch = self.buffer[self.pos];

            if (ch == self.options.escape and self.pos + 1 < self.buffer.len and self.buffer[self.pos + 1] == self.options.quote) {
                // Escaped quote
                try field.append(self.options.quote);
                self.pos += 2;
            } else if (ch == self.options.quote) {
                // End of quoted field
                self.pos += 1;
                break;
            } else {
                try field.append(ch);
                self.pos += 1;
            }
        }

        return field.toOwnedSlice() catch CsvError.OutOfMemory;
    }

    /// Parse an unquoted field
    fn parseUnquotedField(self: *CsvParser) CsvError![]u8 {
        const start = self.pos;

        while (self.pos < self.buffer.len) {
            const ch = self.buffer[self.pos];
            if (ch == self.options.delimiter or ch == '\n' or ch == '\r') {
                break;
            }
            self.pos += 1;
        }

        var field = try self.allocator.dupe(u8, self.buffer[start..self.pos]);

        // Trim if requested
        if (self.options.trim_trailing) {
            var end = field.len;
            while (end > 0 and std.ascii.isWhitespace(field[end - 1])) {
                end -= 1;
            }
            if (end < field.len) {
                field.len = end;
            }
        }

        return field;
    }

    /// Skip whitespace
    fn skipWhitespace(self: *CsvParser) void {
        if (!self.options.trim_leading) return;
        while (self.pos < self.buffer.len and std.ascii.isWhitespace(self.buffer[self.pos])) {
            if (self.buffer[self.pos] == '\n') {
                break; // Don't skip newlines
            }
            self.pos += 1;
        }
    }

    /// Skip to next line
    fn skipLine(self: *CsvParser) void {
        while (self.pos < self.buffer.len) {
            if (self.buffer[self.pos] == '\n') {
                self.pos += 1;
                self.line += 1;
                break;
            }
            if (self.buffer[self.pos] == '\r') {
                self.pos += 1;
                if (self.pos < self.buffer.len and self.buffer[self.pos] == '\n') {
                    self.pos += 1;
                }
                self.line += 1;
                break;
            }
            self.pos += 1;
        }
    }

    /// Skip newline characters
    fn skipNewline(self: *CsvParser) void {
        if (self.pos >= self.buffer.len) return;
        if (self.buffer[self.pos] == '\r') {
            self.pos += 1;
        }
        if (self.pos < self.buffer.len and self.buffer[self.pos] == '\n') {
            self.pos += 1;
        }
        self.line += 1;
    }

    /// Find start of next line
    fn findNextLine(self: CsvParser) usize {
        var pos = self.pos;
        while (pos < self.buffer.len) {
            if (self.buffer[pos] == '\n' or self.buffer[pos] == '\r') {
                return pos;
            }
            pos += 1;
        }
        return pos;
    }
};

/// CSV Writer - for writing CSV data
pub const CsvWriter = struct {
    allocator: std.mem.Allocator,
    options: WriteOptions,
    buffer: std.ArrayList(u8),

    /// Initialize a new CSV writer
    pub fn init(allocator: std.mem.Allocator, options: WriteOptions) CsvWriter {
        return .{
            .allocator = allocator,
            .options = options,
            .buffer = std.ArrayList(u8).init(allocator),
        };
    }

    /// Deinitialize the writer
    pub fn deinit(self: *CsvWriter) void {
        self.buffer.deinit();
    }

    /// Write a header row
    pub fn writeHeader(self: *CsvWriter, headers: []const []const u8) CsvError!void {
        try self.writeRecord(headers);
    }

    /// Write a single record
    pub fn writeRecord(self: *CsvWriter, fields: []const []const u8) CsvError!void {
        for (fields, 0..) |field, i| {
            if (i > 0) {
                try self.buffer.append(self.options.delimiter);
            }
            try self.writeField(field);
        }
        try self.buffer.appendSlice(self.options.line_ending);
    }

    /// Write a single field
    fn writeField(self: *CsvWriter, field: []const u8) CsvError!void {
        const needs_quote = self.options.always_quote or
            (self.options.quote_delimiter and std.mem.indexOfScalar(u8, field, self.options.delimiter) != null) or
            (self.options.quote_quote and std.mem.indexOfScalar(u8, field, self.options.quote) != null) or
            (self.options.quote_newline and (std.mem.indexOfScalar(u8, field, '\n') != null or std.mem.indexOfScalar(u8, field, '\r') != null));

        if (!needs_quote) {
            try self.buffer.appendSlice(field);
            return;
        }

        // Quote the field
        try self.buffer.append(self.options.quote);

        for (field) |ch| {
            if (ch == self.options.quote) {
                // Escape quote by doubling it
                try self.buffer.append(self.options.quote);
            }
            try self.buffer.append(ch);
        }

        try self.buffer.append(self.options.quote);
    }

    /// Get the output string
    pub fn getOutput(self: CsvWriter) []const u8 {
        return self.buffer.items;
    }

    /// Take ownership of the output string
    pub fn toOwnedSlice(self: *CsvWriter) CsvError![]u8 {
        return self.buffer.toOwnedSlice() catch CsvError.OutOfMemory;
    }

    /// Clear the buffer for reuse
    pub fn clear(self: *CsvWriter) void {
        self.buffer.clearRetainingCapacity();
    }
};

/// Convenience function to parse CSV string
pub fn parse(allocator: std.mem.Allocator, input: []const u8, options: ParseOptions) CsvError![]CsvRecord {
    var parser = CsvParser.init(allocator, options);
    return parser.parseAll(input);
}

/// Convenience function to parse CSV with default options
pub fn parseDefault(allocator: std.mem.Allocator, input: []const u8) CsvError![]CsvRecord {
    return parse(allocator, input, .{});
}

/// Convenience function to write records to CSV string
pub fn write(allocator: std.mem.Allocator, records: []const []const []const u8, options: WriteOptions) CsvError![]u8 {
    var writer = CsvWriter.init(allocator, options);
    defer writer.deinit();

    for (records) |record| {
        try writer.writeRecord(record);
    }

    return writer.toOwnedSlice();
}

/// Convenience function to write records with default options
pub fn writeDefault(allocator: std.mem.Allocator, records: []const []const []const u8) CsvError![]u8 {
    return write(allocator, records, .{});
}

/// Free all records from parsing
pub fn freeRecords(allocator: std.mem.Allocator, records: []CsvRecord) void {
    for (records) |*record| {
        record.deinit();
    }
    allocator.free(records);
}

/// Count records in CSV without fully parsing
pub fn countRecords(input: []const u8, options: ParseOptions) usize {
    var count: usize = 0;
    var pos: usize = 0;
    var in_quote = false;

    while (pos < input.len) {
        const ch = input[pos];

        if (ch == options.quote) {
            // Check for escaped quote
            if (pos + 1 < input.len and input[pos + 1] == options.quote) {
                pos += 2;
                continue;
            }
            in_quote = !in_quote;
            pos += 1;
        } else if (!in_quote and (ch == '\n' or ch == '\r')) {
            count += 1;
            // Handle \r\n
            if (ch == '\r' and pos + 1 < input.len and input[pos + 1] == '\n') {
                pos += 2;
            } else {
                pos += 1;
            }
        } else {
            pos += 1;
        }
    }

    // Count last record if no trailing newline
    if (pos > 0 and (input[pos - 1] != '\n' and input[pos - 1] != '\r')) {
        count += 1;
    }

    return count;
}

/// Parse CSV to a 2D string array
pub fn parseToArray(allocator: std.mem.Allocator, input: []const u8, options: ParseOptions) CsvError![][][]u8 {
    const records = try parse(allocator, input, options);
    errdefer freeRecords(allocator, records);

    var result = try allocator.alloc([][]u8, records.len);
    errdefer allocator.free(result);

    for (records, 0..) |*record, i| {
        result[i] = record.fields;
        // Don't deinit the record, just free the records array
    }
    allocator.free(records);

    return result;
}

/// Free a 2D array from parseToArray
pub fn freeArray(allocator: std.mem.Allocator, arr: [][][]u8) void {
    for (arr) |row| {
        for (row) |field| {
            allocator.free(field);
        }
        allocator.free(row);
    }
    allocator.free(arr);
}

// ============================================================================
// Tests
// ============================================================================

test "parse basic CSV" {
    const allocator = std.testing.allocator;
    const input = "name,age,city\nAlice,30,Beijing\nBob,25,Shanghai";

    var records = try parseDefault(allocator, input);
    defer freeRecords(allocator, records);

    try std.testing.expectEqual(@as(usize, 3), records.len);
    try std.testing.expectEqualStrings("name", records[0].get(0).?);
    try std.testing.expectEqualStrings("age", records[0].get(1).?);
    try std.testing.expectEqualStrings("Alice", records[1].get(0).?);
    try std.testing.expectEqual(@as(i64, 30), records[1].asInt(1).?);
    try std.testing.expectEqualStrings("Shanghai", records[2].get(2).?);
}

test "parse quoted fields" {
    const allocator = std.testing.allocator;
    const input = "\"name\",\"age\"\n\"Alice Smith\",\"30\"\n\"Bob \"\"The Builder\"\"\",\"25\"";

    var records = try parseDefault(allocator, input);
    defer freeRecords(allocator, records);

    try std.testing.expectEqual(@as(usize, 3), records.len);
    try std.testing.expectEqualStrings("name", records[0].get(0).?);
    try std.testing.expectEqualStrings("Alice Smith", records[1].get(0).?);
    try std.testing.expectEqualStrings("Bob \"The Builder\"", records[2].get(0).?);
}

test "parse with different delimiter" {
    const allocator = std.testing.allocator;
    const input = "name;age;city\nAlice;30;Beijing";

    var records = try parse(allocator, input, .{ .delimiter = ';' });
    defer freeRecords(allocator, records);

    try std.testing.expectEqual(@as(usize, 2), records.len);
    try std.testing.expectEqualStrings("name", records[0].get(0).?);
    try std.testing.expectEqualStrings("city", records[0].get(2).?);
}

test "parse with comments" {
    const allocator = std.testing.allocator;
    const input = "# This is a comment\nname,age\nAlice,30\n# Another comment\nBob,25";

    var records = try parse(allocator, input, .{ .comment = '#' });
    defer freeRecords(allocator, records);

    try std.testing.expectEqual(@as(usize, 3), records.len);
    try std.testing.expectEqualStrings("name", records[0].get(0).?);
    try std.testing.expectEqualStrings("Alice", records[1].get(0).?);
    try std.testing.expectEqualStrings("Bob", records[2].get(0).?);
}

test "parse empty fields" {
    const allocator = std.testing.allocator;
    const input = "a,b,c\n1,,3\n,2,";

    const records = try parseDefault(allocator, input);
    defer freeRecords(allocator, records);

    try std.testing.expectEqual(@as(usize, 3), records.len);
    try std.testing.expectEqual(@as(usize, 3), records[0].count());
    try std.testing.expectEqual(@as(usize, 3), records[1].count());
    try std.testing.expectEqual(@as(usize, 3), records[2].count());
    try std.testing.expectEqualStrings("", records[1].get(1).?);
    try std.testing.expectEqualStrings("", records[2].get(0).?);
    try std.testing.expectEqualStrings("", records[2].get(2).?);
}

test "write basic CSV" {
    const allocator = std.testing.allocator;
    const records = [_][]const []const u8{
        &[_][]const u8{ "name", "age", "city" },
        &[_][]const u8{ "Alice", "30", "Beijing" },
        &[_][]const u8{ "Bob", "25", "Shanghai" },
    };

    const output = try writeDefault(allocator, &records);
    defer allocator.free(output);

    try std.testing.expectEqualStrings("name,age,city\nAlice,30,Beijing\nBob,25,Shanghai\n", output);
}

test "write with quoted fields" {
    const allocator = std.testing.allocator;
    const records = [_][]const []const u8{
        &[_][]const u8{ "name", "description" },
        &[_][]const u8{ "Alice", "She said, \"Hello\"" },
    };

    const output = try writeDefault(allocator, &records);
    defer allocator.free(output);

    try std.testing.expect(std.mem.indexOf(u8, output, "\"She said, \"\"Hello\"\"\"") != null);
}

test "write with always quote option" {
    const allocator = std.testing.allocator;
    const records = [_][]const []const u8{
        &[_][]const u8{ "a", "b" },
        &[_][]const u8{ "1", "2" },
    };

    const output = try write(allocator, &records, .{ .always_quote = true });
    defer allocator.free(output);

    try std.testing.expectEqualStrings("\"a\",\"b\"\n\"1\",\"2\"\n", output);
}

test "roundtrip parse and write" {
    const allocator = std.testing.allocator;
    const input = "name,age,city\nAlice,30,Beijing\nBob,25,Shanghai\n";

    // Parse
    const records = try parseDefault(allocator, input);
    defer freeRecords(allocator, records);

    // Write back
    var record_slices = std.ArrayList([]const []const u8).init(allocator);
    defer record_slices.deinit();

    for (records) |record| {
        try record_slices.append(record.fields);
    }

    const output = try writeDefault(allocator, record_slices.items);
    defer allocator.free(output);

    try std.testing.expectEqualStrings(input, output);
}

test "parse with newlines in quoted fields" {
    const allocator = std.testing.allocator;
    const input = "name,description\n\"Alice\",\"Line1\nLine2\"";

    var records = try parseDefault(allocator, input);
    defer freeRecords(allocator, records);

    try std.testing.expectEqual(@as(usize, 2), records.len);
    try std.testing.expectEqualStrings("Line1\nLine2", records[1].get(1).?);
}

test "count records" {
    const input = "a,b,c\n1,2,3\n4,5,6";
    const count = countRecords(input, .{});
    try std.testing.expectEqual(@as(usize, 3), count);
}

test "CsvRecord helper methods" {
    const allocator = std.testing.allocator;

    var fields = try allocator.alloc([]u8, 4);
    fields[0] = try allocator.dupe(u8, "Alice");
    fields[1] = try allocator.dupe(u8, "30");
    fields[2] = try allocator.dupe(u8, "3.14159");
    fields[3] = try allocator.dupe(u8, "true");

    var record = CsvRecord.init(allocator, fields);
    defer record.deinit();

    try std.testing.expectEqual(@as(usize, 4), record.count());
    try std.testing.expectEqualStrings("Alice", record.get(0).?);
    try std.testing.expectEqual(@as(i64, 30), record.asInt(1).?);
    try std.testing.expectApproxEqAbs(@as(f64, 3.14159), record.asFloat(2).?, 0.0001);
    try std.testing.expectEqual(true, record.asBool(3).?);
    try std.testing.expectEqual(@as(?i64, null), record.asInt(0)); // Not a number
    try std.testing.expectEqual(@as(?[]const u8, null), record.get(10)); // Out of bounds
}

test "parse with field count validation" {
    const allocator = std.testing.allocator;
    const input = "a,b,c\n1,2,3\n4,5"; // Last row has wrong count

    const records = parse(allocator, input, .{ .expected_fields = 3 });
    try std.testing.expectError(CsvError.FieldCountMismatch, records);
}

test "parse empty input" {
    const allocator = std.testing.allocator;

    const records = try parseDefault(allocator, "");
    defer freeRecords(allocator, records);

    try std.testing.expectEqual(@as(usize, 0), records.len);
}

test "parse single row" {
    const allocator = std.testing.allocator;
    const input = "a,b,c";

    var records = try parseDefault(allocator, input);
    defer freeRecords(allocator, records);

    try std.testing.expectEqual(@as(usize, 1), records.len);
    try std.testing.expectEqual(@as(usize, 3), records[0].count());
}

test "parse with CRLF line endings" {
    const allocator = std.testing.allocator;
    const input = "name,age\r\nAlice,30\r\nBob,25\r\n";

    var records = try parseDefault(allocator, input);
    defer freeRecords(allocator, records);

    try std.testing.expectEqual(@as(usize, 3), records.len);
    try std.testing.expectEqualStrings("Alice", records[1].get(0).?);
}

test "CsvWriter with custom line ending" {
    const allocator = std.testing.allocator;
    const records = [_][]const []const u8{
        &[_][]const u8{ "a", "b" },
    };

    const output = try write(allocator, &records, .{ .line_ending = "\r\n" });
    defer allocator.free(output);

    try std.testing.expectEqualStrings("a,b\r\n", output);
}

test "parseToArray and freeArray" {
    const allocator = std.testing.allocator;
    const input = "a,b\n1,2\n3,4";

    const arr = try parseToArray(allocator, input, .{});
    defer freeArray(allocator, arr);

    try std.testing.expectEqual(@as(usize, 3), arr.len);
    try std.testing.expectEqual(@as(usize, 2), arr[0].len);
    try std.testing.expectEqualStrings("a", arr[0][0]);
    try std.testing.expectEqualStrings("4", arr[2][1]);
}