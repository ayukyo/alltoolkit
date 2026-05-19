const std = @import("std");
const morse = @import("morse_code_utils");

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    std.debug.print("=== Zig Morse Code Utils Examples ===\n\n", .{});

    // Encoding examples
    std.debug.print("--- Encoding Examples ---\n", .{});
    {
        const encoded = try morse.encode(allocator, "SOS");
        defer allocator.free(encoded);
        std.debug.print("encode(\"SOS\") = {s}\n", .{encoded});

        const encoded2 = try morse.encode(allocator, "HELLO WORLD");
        defer allocator.free(encoded2);
        std.debug.print("encode(\"HELLO WORLD\") = {s}\n", .{encoded2});

        const encoded3 = try morse.encode(allocator, "123");
        defer allocator.free(encoded3);
        std.debug.print("encode(\"123\") = {s}\n", .{encoded3});

        const encoded4 = try morse.encode(allocator, "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG");
        defer allocator.free(encoded4);
        std.debug.print("encode(\"THE QUICK BROWN FOX...\") = {s}\n", .{encoded4});
    }

    std.debug.print("\n", .{});

    // Decoding examples
    std.debug.print("--- Decoding Examples ---\n", .{});
    {
        const decoded = try morse.decode(allocator, "... --- ...");
        defer allocator.free(decoded);
        std.debug.print("decode(\"... --- ...\") = {s}\n", .{decoded});

        const decoded2 = try morse.decode(allocator, ".... . .-.. .-.. --- / .-- --- .-. .-.. -..");
        defer allocator.free(decoded2);
        std.debug.print("decode(\".... . .-.. .-.. --- / .-- --- .-. .-.. -..\") = {s}\n", .{decoded2});
    }

    std.debug.print("\n", .{});

    // Roundtrip test
    std.debug.print("--- Roundtrip Test ---\n", .{});
    {
        const original = "HELLO";
        const encoded = try morse.encode(allocator, original);
        defer allocator.free(encoded);
        const decoded = try morse.decode(allocator, encoded);
        defer allocator.free(decoded);
        std.debug.print("Original: {s}\n", .{original});
        std.debug.print("Encoded: {s}\n", .{encoded});
        std.debug.print("Decoded: {s}\n", .{decoded});
        std.debug.print("Match: {}\n", .{std.mem.eql(u8, original, decoded)});
    }

    std.debug.print("\n", .{});

    // Punctuation
    std.debug.print("--- Punctuation Support ---\n", .{});
    {
        const encoded = try morse.encode(allocator, "HI!");
        defer allocator.free(encoded);
        std.debug.print("encode(\"HI!\") = {s}\n", .{encoded});

        const encoded2 = try morse.encode(allocator, "WHAT?");
        defer allocator.free(encoded2);
        std.debug.print("encode(\"WHAT?\") = {s}\n", .{encoded2});

        const encoded3 = try morse.encode(allocator, "HELLO, WORLD.");
        defer allocator.free(encoded3);
        std.debug.print("encode(\"HELLO, WORLD.\") = {s}\n", .{encoded3});
    }

    std.debug.print("\n", .{});

    // Custom separator
    std.debug.print("--- Custom Word Separator ---\n", .{});
    {
        const encoded = try morse.encodeWithSeparator(allocator, "HELLO WORLD", " | ");
        defer allocator.free(encoded);
        std.debug.print("encodeWithSeparator(\"HELLO WORLD\", \" | \") = {s}\n", .{encoded});
    }

    std.debug.print("\n", .{});

    // Signal generation
    std.debug.print("--- Signal Generation ---\n", .{});
    {
        const timing = morse.Timing{
            .dot_duration_ms = 100,
            .dash_duration_ms = 300,
            .intra_char_gap_ms = 100,
            .inter_char_gap_ms = 300,
            .word_gap_ms = 700,
        };

        const signals = try morse.generateSignals(allocator, ".-", timing);
        defer morse.freeSignals(allocator, signals);

        std.debug.print("Signal sequence for \".-\":\n", .{});
        for (signals, 0..) |signal, i| {
            std.debug.print("  [{d}] {} for {d}ms\n", .{ i, signal.active, signal.duration_ms });
        }
    }

    std.debug.print("\n", .{});

    // Utility functions
    std.debug.print("--- Utility Functions ---\n", .{});
    {
        std.debug.print("isEncodable('A') = {}\n", .{morse.isEncodable('A')});
        std.debug.print("isEncodable('~') = {}\n", .{morse.isEncodable('~')});

        const count = morse.countEncodable("HELLO 123!");
        std.debug.print("countEncodable(\"HELLO 123!\") = {d}\n", .{count});

        const symbols = morse.countSymbols("... --- ...");
        std.debug.print("countSymbols(\"... --- ...\"): dots={d}, dashes={d}\n", .{ symbols.dots, symbols.dashes });

        const visual = try morse.formatVisual(allocator, "... --- ...", '*', '-');
        defer allocator.free(visual);
        std.debug.print("formatVisual with custom chars: {s}\n", .{visual});
    }

    std.debug.print("\n", .{});

    // Duration calculation
    std.debug.print("--- Duration Calculation ---\n", .{});
    {
        const timing = morse.Timing{
            .dot_duration_ms = 60,
            .dash_duration_ms = 180,
            .intra_char_gap_ms = 60,
            .inter_char_gap_ms = 180,
            .word_gap_ms = 420,
        };

        const encoded = try morse.encode(allocator, "SOS");
        defer allocator.free(encoded);

        const duration_ms = morse.calculateDuration(encoded, timing);
        std.debug.print("Morse code: {s}\n", .{encoded});
        std.debug.print("Duration: {d}ms ({d}s)\n", .{ duration_ms, @as(f64, @floatFromInt(duration_ms)) / 1000.0 });
    }

    std.debug.print("\n", .{});

    // Analysis
    std.debug.print("--- Analysis ---\n", .{});
    {
        const timing = morse.Timing{};
        const stats = try morse.analyze(allocator, "HELLO WORLD", timing);

        std.debug.print("Text analysis:\n", .{});
        std.debug.print("  Total characters: {d}\n", .{stats.total_chars});
        std.debug.print("  Encodable characters: {d}\n", .{stats.encodable_chars});
        std.debug.print("  Dots: {d}\n", .{stats.dots});
        std.debug.print("  Dashes: {d}\n", .{stats.dashes});
        std.debug.print("  Letters: {d}\n", .{stats.letters});
        std.debug.print("  Words: {d}\n", .{stats.words});
        std.debug.print("  Estimated duration: {d}ms\n", .{stats.estimated_duration_ms});
    }

    std.debug.print("\n", .{});

    // Validation
    std.debug.print("--- Validation ---\n", .{});
    {
        std.debug.print("isValidMorse(\"... --- ...\") = {}\n", .{morse.isValidMorse("... --- ...")});
        std.debug.print("isValidMorse(\".abc\") = {}\n", .{morse.isValidMorse(".abc")});

        const cleaned = try morse.cleanMorse(allocator, "... x --- x ...");
        defer allocator.free(cleaned);
        std.debug.print("cleanMorse(\"... x --- x ...\") = {s}\n", .{cleaned});
    }

    std.debug.print("\n", .{});

    // Emergency signal
    std.debug.print("--- Emergency Signal ---\n", .{});
    {
        const sos = try morse.encodeSOS(allocator);
        defer allocator.free(sos);
        std.debug.print("SOS signal: {s}\n", .{sos});
        std.debug.print("SOS is the international distress signal!\n", .{});
    }

    std.debug.print("\n=== All examples completed ===\n", .{});
}