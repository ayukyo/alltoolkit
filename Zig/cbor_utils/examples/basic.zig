const std = @import("std");
const cbor = @import("cbor");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== CBOR Encoding/Decoding Examples ===\n\n", .{});

    // Example 1: Encoding simple values
    std.debug.print("1. Encoding simple values:\n", .{});

    var buffer: [256]u8 = undefined;
    var encoder = cbor.Encoder.init(&buffer);

    // Encode integer
    try encoder.encode(cbor.Value{ .positive_int = 42 });
    std.debug.print("  Integer 42: ", .{});
    printHex(encoder.encoded());
    encoder.pos = 0;

    // Encode text string
    try encoder.encode(cbor.Value{ .text_string = "Hello, CBOR!" });
    std.debug.print("  Text \"Hello, CBOR!\": ", .{});
    printHex(encoder.encoded());
    encoder.pos = 0;

    // Encode boolean
    try encoder.encode(cbor.Value{ .simple = .true_val });
    std.debug.print("  Boolean true: ", .{});
    printHex(encoder.encoded());
    encoder.pos = 0;

    // Encode null
    try encoder.encode(cbor.Value{ .simple = .null_val });
    std.debug.print("  Null: ", .{});
    printHex(encoder.encoded());
    encoder.pos = 0;

    std.debug.print("\n", .{});

    // Example 2: Encoding arrays
    std.debug.print("2. Encoding arrays:\n", .{});

    var arr = try allocator.alloc(cbor.Value, 4);
    arr[0] = cbor.Value{ .positive_int = 1 };
    arr[1] = cbor.Value{ .positive_int = 2 };
    arr[2] = cbor.Value{ .positive_int = 3 };
    arr[3] = cbor.Value{ .positive_int = 4 };

    try encoder.encode(cbor.Value{ .array = arr });
    std.debug.print("  Array [1, 2, 3, 4]: ", .{});
    printHex(encoder.encoded());
    encoder.pos = 0;

    // Mixed type array
    var mixed_arr = try allocator.alloc(cbor.Value, 3);
    mixed_arr[0] = cbor.Value{ .text_string = "foo" };
    mixed_arr[1] = cbor.Value{ .simple = .false_val };
    mixed_arr[2] = cbor.Value{ .positive_int = 100 };

    try encoder.encode(cbor.Value{ .array = mixed_arr });
    std.debug.print("  Mixed array: ", .{});
    printHex(encoder.encoded());
    encoder.pos = 0;

    allocator.free(arr);
    allocator.free(mixed_arr);

    std.debug.print("\n", .{});

    // Example 3: Encoding maps
    std.debug.print("3. Encoding maps:\n", .{});

    var entries = try allocator.alloc(cbor.MapEntry, 3);
    entries[0] = .{
        .key = cbor.Value{ .text_string = "name" },
        .value = cbor.Value{ .text_string = "Alice" },
    };
    entries[1] = .{
        .key = cbor.Value{ .text_string = "age" },
        .value = cbor.Value{ .positive_int = 30 },
    };
    entries[2] = .{
        .key = cbor.Value{ .text_string = "active" },
        .value = cbor.Value{ .simple = .true_val },
    };

    try encoder.encode(cbor.Value{ .map = entries });
    std.debug.print("  Map: ", .{});
    printHex(encoder.encoded());
    encoder.pos = 0;

    allocator.free(entries);

    std.debug.print("\n", .{});

    // Example 4: Encoding floats
    std.debug.print("4. Encoding floats:\n", .{});

    try encoder.encode(cbor.Value{ .float = 3.141592653589793 });
    std.debug.print("  Pi (double): ", .{});
    printHex(encoder.encoded());
    encoder.pos = 0;

    try encoder.encode(cbor.Value{ .float = -1.5 });
    std.debug.print("  -1.5: ", .{});
    printHex(encoder.encoded());
    encoder.pos = 0;

    std.debug.print("\n", .{});

    // Example 5: Decoding
    std.debug.print("5. Decoding examples:\n", .{});

    // Decode small integer (<= 23)
    const int_data = [_]u8{0x0A}; // 10
    var decoder = cbor.Decoder.init(&int_data, allocator);
    const int_val = try decoder.decode();
    std.debug.print("  Decoded small integer (10): {}\n", .{int_val.positive_int});

    // Decode larger integer (> 23)
    const int_data2 = [_]u8{ 0x18, 0x2A }; // 42
    decoder = cbor.Decoder.init(&int_data2, allocator);
    const int_val2 = try decoder.decode();
    std.debug.print("  Decoded larger integer (42): {}\n", .{int_val2.positive_int});

    // Decode string
    const str_data = [_]u8{ 0x65, 'h', 'e', 'l', 'l', 'o' };
    decoder = cbor.Decoder.init(&str_data, allocator);
    const str_val = try decoder.decode();
    defer str_val.deinit(allocator);
    std.debug.print("  Decoded string: \"{s}\"\n", .{str_val.text_string});

    // Decode array
    const arr_data = [_]u8{ 0x83, 0x01, 0x02, 0x03 };
    decoder = cbor.Decoder.init(&arr_data, allocator);
    const arr_val = try decoder.decode();
    defer arr_val.deinit(allocator);
    std.debug.print("  Decoded array: [", .{});
    for (arr_val.array, 0..) |item, i| {
        if (i > 0) std.debug.print(", ", .{});
        std.debug.print("{}", .{item.positive_int});
    }
    std.debug.print("]\n", .{});

    std.debug.print("\n", .{});

    // Example 6: Roundtrip
    std.debug.print("6. Roundtrip encoding/decoding:\n", .{});

    // Create a complex structure
    var inner_arr = try allocator.alloc(cbor.Value, 2);
    inner_arr[0] = cbor.Value{ .positive_int = 10 };
    inner_arr[1] = cbor.Value{ .positive_int = 20 };

    var outer_entries = try allocator.alloc(cbor.MapEntry, 2);
    outer_entries[0] = .{
        .key = cbor.Value{ .text_string = "values" },
        .value = cbor.Value{ .array = inner_arr },
    };
    outer_entries[1] = .{
        .key = cbor.Value{ .text_string = "status" },
        .value = cbor.Value{ .simple = .null_val },
    };

    const original = cbor.Value{ .map = outer_entries };

    // Encode
    const encoded = try cbor.encode(allocator, original);
    defer allocator.free(encoded);

    std.debug.print("  Encoded: ", .{});
    printHex(encoded);

    // Decode
    var rt_decoder = cbor.Decoder.init(encoded, allocator);
    const decoded = try rt_decoder.decode();
    defer decoded.deinit(allocator);

    // Convert to JSON for display
    const json = try decoded.toJson(allocator);
    defer allocator.free(json);
    std.debug.print("  As JSON: {s}\n", .{json});

    allocator.free(outer_entries);

    std.debug.print("\n=== All examples completed! ===\n", .{});
}

fn printHex(data: []const u8) void {
    std.debug.print("[", .{});
    for (data, 0..) |byte, i| {
        if (i > 0) std.debug.print(", ", .{});
        std.debug.print("0x{X:0>2}", .{byte});
    }
    std.debug.print("]\n", .{});
}