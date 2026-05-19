const std = @import("std");
const luhn = @import("luhn_utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== Luhn Algorithm Utilities Example ===\n\n", .{});

    // Test card numbers (these are test numbers, not real cards)
    const test_cards = [_][]const u8{
        "4242424242424242", // Visa
        "5555555555554444", // Mastercard
        "378282246310005", // Amex
        "6011111111111117", // Discover
        "3530111333300000", // JCB
        "4111111111111111", // Visa
        "1234567890123456", // Invalid
    };

    std.debug.print("--- Card Validation Examples ---\n\n", .{});

    for (test_cards) |card| {
        const is_valid = luhn.validate(card) catch false;
        const card_type = luhn.detectCardType(card);

        std.debug.print("Card: {s}\n", .{card});
        std.debug.print("  Type: {s}\n", .{card_type.name()});
        std.debug.print("  Valid: {}\n\n", .{is_valid});
    }

    // Detailed validation
    std.debug.print("--- Detailed Validation ---\n\n", .{});

    var result = try luhn.validateWithDetails(allocator, "4242424242424242");
    defer result.deinit(allocator);

    std.debug.print("Card: {s}\n", .{result.formatted_number});
    std.debug.print("  Type: {s}\n", .{result.card_type.name()});
    std.debug.print("  Valid: {}\n", .{result.is_valid});
    std.debug.print("  Check digit: {} (computed: {})\n\n", .{ result.check_digit, result.computed_check_digit });

    // Calculate check digit
    std.debug.print("--- Check Digit Calculation ---\n\n", .{});

    const numbers_without_check = [_][]const u8{
        "7992739871",
        "424242424242424",
        "555555555555444",
    };

    for (numbers_without_check) |num| {
        const check_digit = try luhn.calculateCheckDigit(num);
        std.debug.print("Number: {s}\n", .{num});
        std.debug.print("  Check digit: {} (full: {s}{d})\n\n", .{ check_digit, num, check_digit });
    }

    // IMEI validation
    std.debug.print("--- IMEI Validation ---\n\n", .{});

    const imeis = [_][]const u8{
        "490154203237518", // Valid
        "490154203237519", // Invalid
    };

    for (imeis) |imei| {
        const is_valid = luhn.validateIMEI(imei) catch false;
        std.debug.print("IMEI: {s} - {}\n", .{ imei, is_valid });
    }

    // Canadian SIN validation
    std.debug.print("\n--- Canadian SIN Validation ---\n\n", .{});

    const sins = [_][]const u8{
        "046454286", // Valid
        "046454287", // Invalid
    };

    for (sins) |sin| {
        const is_valid = luhn.validateCanadianSIN(sin) catch false;
        std.debug.print("SIN: {s} - {}\n", .{ sin, is_valid });
    }

    // Generate test number
    std.debug.print("\n--- Test Number Generation ---\n\n", .{});

    const generated = try luhn.generateTestNumber(allocator, "4242", 16);
    defer allocator.free(generated);

    std.debug.print("Generated Visa-like number: {s}\n", .{generated});
    std.debug.print("  Valid: {}\n", .{try luhn.validate(generated)});

    // Format number
    std.debug.print("\n--- Number Formatting ---\n\n", .{});

    const formatted = try luhn.formatNumber(allocator, "4242424242424242", 4);
    defer allocator.free(formatted);

    std.debug.print("Original: 4242424242424242\n", .{});
    std.debug.print("Formatted: {s}\n", .{formatted});

    // Clean number
    std.debug.print("\n--- Number Cleaning ---\n\n", .{});

    const cleaned = try luhn.cleanNumber(allocator, "4242-4242-4242-4242");
    defer allocator.free(cleaned);

    std.debug.print("Original: 4242-4242-4242-4242\n", .{});
    std.debug.print("Cleaned: {s}\n", .{cleaned});

    std.debug.print("\n=== All examples completed! ===\n", .{});
}