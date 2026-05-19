const std = @import("std");

/// Morse code operation errors
pub const MorseError = error{
    OutOfMemory,
    InvalidCharacter,
    InvalidMorseCode,
    EmptyInput,
};

/// Standard timing units for Morse code
/// - Dot = 1 unit
/// - Dash = 3 units
/// - Space between parts of same letter = 1 unit
/// - Space between letters = 3 units
/// - Space between words = 7 units
pub const Timing = struct {
    dot_duration_ms: u32 = 100,
    dash_duration_ms: u32 = 300,
    intra_char_gap_ms: u32 = 100,
    inter_char_gap_ms: u32 = 300,
    word_gap_ms: u32 = 700,
};

/// Morse code lookup table (A-Z, 0-9, and common punctuation)
const MORSE_CODE = [_][]const u8{
    ".-",    // A
    "-...",  // B
    "-.-.",  // C
    "-..",   // D
    ".",     // E
    "..-.",  // F
    "--.",   // G
    "....",  // H
    "..",    // I
    ".---",  // J
    "-.-",   // K
    ".-..",  // L
    "--",    // M
    "-.",    // N
    "---",   // O
    ".--.",  // P
    "--.-",  // Q
    ".-.",   // R
    "...",   // S
    "-",     // T
    "..-",   // U
    "...-",  // V
    ".--",   // W
    "-..-",  // X
    "-.--",  // Y
    "--..",  // Z
    "-----", // 0
    ".----", // 1
    "..---", // 2
    "...--", // 3
    "....-", // 4
    ".....", // 5
    "-....", // 6
    "--...", // 7
    "---..", // 8
    "----.", // 9
    ".-.-.-", // . (period)
    "--..--", // , (comma)
    "..--..", // ? (question mark)
    ".----.", // ' (apostrophe)
    "-.-.--", // ! (exclamation)
    "-..-.",  // / (slash)
    "-.--.",  // ( (left parenthesis)
    "-.--.-", // ) (right parenthesis)
    ".-...",  // & (ampersand)
    "---...", // : (colon)
    "-.-.-.", // ; (semicolon)
    "-...-",  // = (equals)
    ".-.-.",  // + (plus)
    "-....-", // - (hyphen)
    "..--.-", // _ (underscore)
    ".-..-.", // " (quote)
    "...-..-", // $ (dollar)
    ".--.-.",  // @ (at sign)
};

/// Character indices in MORSE_CODE
const CHAR_INDEX_A: usize = 0;
const CHAR_INDEX_Z: usize = 25;
const CHAR_INDEX_0: usize = 26;
const CHAR_INDEX_9: usize = 35;
const CHAR_INDEX_PERIOD: usize = 36;
const CHAR_INDEX_AT: usize = 51;

/// Get character index in the MORSE_CODE table
fn getCharIndex(c: u8) ?usize {
    return switch (c) {
        'A'...'Z' => @as(usize, c - 'A'),
        'a'...'z' => @as(usize, c - 'a'),
        '0'...'9' => @as(usize, c - '0' + 26),
        '.' => 36,
        ',' => 37,
        '?' => 38,
        '\'' => 39,
        '!' => 40,
        '/' => 41,
        '(' => 42,
        ')' => 43,
        '&' => 44,
        ':' => 45,
        ';' => 46,
        '=' => 47,
        '+' => 48,
        '-' => 49,
        '_' => 50,
        '"' => 51,
        '$' => 52,
        '@' => 53,
        else => null,
    };
}

/// Reverse lookup: morse code to character
/// Returns null if not found
fn morseToChar(code: []const u8) ?u8 {
    for (MORSE_CODE, 0..) |morse, i| {
        if (std.mem.eql(u8, morse, code)) {
            return indexToChar(i);
        }
    }
    return null;
}

/// Convert index to character
fn indexToChar(index: usize) ?u8 {
    return switch (index) {
        0...25 => @as(u8, @intCast('A' + index)),
        26...35 => @as(u8, @intCast('0' + (index - 26))),
        36 => '.',
        37 => ',',
        38 => '?',
        39 => '\'',
        40 => '!',
        41 => '/',
        42 => '(',
        43 => ')',
        44 => '&',
        45 => ':',
        46 => ';',
        47 => '=',
        48 => '+',
        49 => '-',
        50 => '_',
        51 => '"',
        52 => '$',
        53 => '@',
        else => null,
    };
}

// ============================================================================
// Encoding Functions
// ============================================================================

/// Encode a single character to Morse code
/// Returns null if character is not supported
pub fn encodeChar(c: u8) ?[]const u8 {
    const index = getCharIndex(c) orelse return null;
    return MORSE_CODE[index];
}

/// Encode a string to Morse code
/// Uses '/' as word separator
pub fn encode(allocator: std.mem.Allocator, text: []const u8) MorseError![]u8 {
    if (text.len == 0) {
        return MorseError.EmptyInput;
    }

    var result = std.ArrayList(u8).init(allocator);
    errdefer result.deinit();

    var last_was_word_sep = false;
    var first_char = true;

    for (text) |c| {
        if (c == ' ') {
            // Word separator - only add if we have some encoded content
            if (!first_char and !last_was_word_sep) {
                try result.appendSlice(" / ");
                last_was_word_sep = true;
            }
            continue;
        }

        const morse = encodeChar(c) orelse {
            // Skip unsupported characters
            continue;
        };

        // Add space before letter if not first and not after word separator
        if (!first_char and !last_was_word_sep) {
            try result.append(' ');
        }

        try result.appendSlice(morse);
        first_char = false;
        last_was_word_sep = false;
    }

    return result.toOwnedSlice();
}

/// Encode a string to Morse code with custom word separator
pub fn encodeWithSeparator(allocator: std.mem.Allocator, text: []const u8, word_sep: []const u8) MorseError![]u8 {
    if (text.len == 0) {
        return MorseError.EmptyInput;
    }

    var result = std.ArrayList(u8).init(allocator);
    errdefer result.deinit();

    var first_char = true;
    var prev_was_space = false;

    for (text) |c| {
        if (c == ' ') {
            if (!prev_was_space and !first_char) {
                try result.appendSlice(word_sep);
            }
            prev_was_space = true;
            continue;
        }

        const morse = encodeChar(c) orelse continue;

        if (!first_char and !prev_was_space) {
            try result.append(' ');
        }

        try result.appendSlice(morse);
        first_char = false;
        prev_was_space = false;
    }

    return result.toOwnedSlice();
}

// ============================================================================
// Decoding Functions
// ============================================================================

/// Decode a Morse code string back to text
/// Expects space between letters and '/' or '   ' between words
pub fn decode(allocator: std.mem.Allocator, morse: []const u8) MorseError![]u8 {
    if (morse.len == 0) {
        return MorseError.EmptyInput;
    }

    var result = std.ArrayList(u8).init(allocator);
    errdefer result.deinit();

    var iter = std.mem.split(u8, morse, " ");
    var prev_was_word_sep = false;

    while (iter.next()) |code| {
        if (code.len == 0) {
            // Multiple spaces indicate word separator
            if (!prev_was_word_sep and result.items.len > 0) {
                try result.append(' ');
                prev_was_word_sep = true;
            }
            continue;
        }

        // Check for explicit word separator
        if (std.mem.eql(u8, code, "/")) {
            if (!prev_was_word_sep and result.items.len > 0) {
                try result.append(' ');
                prev_was_word_sep = true;
            }
            continue;
        }

        const char = morseToChar(code) orelse {
            // Skip invalid Morse code
            continue;
        };

        try result.append(char);
        prev_was_word_sep = false;
    }

    return result.toOwnedSlice();
}

/// Decode a Morse code string with custom separators
pub fn decodeWithSeparators(allocator: std.mem.Allocator, morse: []const u8, letter_sep: []const u8, word_sep: []const u8) MorseError![]u8 {
    if (morse.len == 0) {
        return MorseError.EmptyInput;
    }

    var result = std.ArrayList(u8).init(allocator);
    errdefer result.deinit();

    // Split by word separator first
    var word_iter = std.mem.split(u8, morse, word_sep);

    var first_word = true;
    while (word_iter.next()) |word| {
        if (word.len == 0) continue;

        if (!first_word) {
            try result.append(' ');
        }
        first_word = false;

        // Split word by letter separator
        var letter_iter = std.mem.split(u8, word, letter_sep);
        while (letter_iter.next()) |code| {
            if (code.len == 0) continue;

            const char = morseToChar(code) orelse continue;
            try result.append(char);
        }
    }

    return result.toOwnedSlice();
}

// ============================================================================
// Signal Generation
// ============================================================================

/// Represents a signal element (on or off)
pub const SignalElement = struct {
    active: bool,
    duration_ms: u32,
};

/// Generate signal sequence for playing Morse code
/// Returns an array of on/off signals with durations
pub fn generateSignals(allocator: std.mem.Allocator, morse: []const u8, timing: Timing) MorseError![]SignalElement {
    var signals = std.ArrayList(SignalElement).init(allocator);
    errdefer signals.deinit();

    for (morse) |c| {
        switch (c) {
            '.' => {
                // Dot
                try signals.append(.{ .active = true, .duration_ms = timing.dot_duration_ms });
                try signals.append(.{ .active = false, .duration_ms = timing.intra_char_gap_ms });
            },
            '-' => {
                // Dash
                try signals.append(.{ .active = true, .duration_ms = timing.dash_duration_ms });
                try signals.append(.{ .active = false, .duration_ms = timing.intra_char_gap_ms });
            },
            ' ' => {
                // Remove last intra-char gap and add inter-char gap
                if (signals.items.len > 0) {
                    _ = signals.pop();
                    try signals.append(.{ .active = false, .duration_ms = timing.inter_char_gap_ms });
                }
            },
            '/' => {
                // Word separator
                if (signals.items.len > 0) {
                    _ = signals.pop();
                    try signals.append(.{ .active = false, .duration_ms = timing.word_gap_ms });
                }
            },
            else => {},
        }
    }

    return signals.toOwnedSlice();
}

/// Free signal array
pub fn freeSignals(allocator: std.mem.Allocator, signals: []SignalElement) void {
    allocator.free(signals);
}

// ============================================================================
// Utility Functions
// ============================================================================

/// Check if a character is encodable in Morse code
pub fn isEncodable(c: u8) bool {
    return getCharIndex(c) != null;
}

/// Count encodable characters in a string
pub fn countEncodable(text: []const u8) usize {
    var count: usize = 0;
    for (text) |c| {
        if (isEncodable(c)) {
            count += 1;
        }
    }
    return count;
}

/// Calculate total duration of Morse code in milliseconds
pub fn calculateDuration(morse: []const u8, timing: Timing) u64 {
    var total: u64 = 0;

    for (morse) |c| {
        switch (c) {
            '.' => total += timing.dot_duration_ms + timing.intra_char_gap_ms,
            '-' => total += timing.dash_duration_ms + timing.intra_char_gap_ms,
            ' ' => total += timing.inter_char_gap_ms,
            '/' => total += timing.word_gap_ms,
            else => {},
        }
    }

    return total;
}

/// Get the number of Morse code symbols (dots and dashes) in a code
pub fn countSymbols(morse: []const u8) struct { dots: usize, dashes: usize } {
    var dots: usize = 0;
    var dashes: usize = 0;

    for (morse) |c| {
        switch (c) {
            '.' => dots += 1,
            '-' => dashes += 1,
            else => {},
        }
    }

    return .{ .dots = dots, .dashes = dashes };
}

/// Format Morse code with visual representation
/// Returns a string with dots and dashes replaced by visual characters
pub fn formatVisual(allocator: std.mem.Allocator, morse: []const u8, dot_char: u8, dash_char: u8) MorseError![]u8 {
    var result = std.ArrayList(u8).init(allocator);
    errdefer result.deinit();

    for (morse) |c| {
        switch (c) {
            '.' => try result.append(dot_char),
            '-' => try result.append(dash_char),
            else => try result.append(c),
        }
    }

    return result.toOwnedSlice();
}

/// Convert text to SOS signal (emergency signal)
pub fn encodeSOS(allocator: std.mem.Allocator) MorseError![]u8 {
    return encode(allocator, "SOS");
}

/// Validate Morse code string
pub fn isValidMorse(morse: []const u8) bool {
    for (morse) |c| {
        switch (c) {
            '.', '-', ' ', '/' => {},
            else => return false,
        }
    }
    return true;
}

/// Clean Morse code (remove invalid characters)
pub fn cleanMorse(allocator: std.mem.Allocator, morse: []const u8) MorseError![]u8 {
    var result = std.ArrayList(u8).init(allocator);
    errdefer result.deinit();

    for (morse) |c| {
        switch (c) {
            '.', '-', ' ', '/' => try result.append(c),
            else => {},
        }
    }

    return result.toOwnedSlice();
}

// ============================================================================
// Statistics and Analysis
// ============================================================================

/// Analyze Morse code properties
pub const MorseStats = struct {
    total_chars: usize,
    encodable_chars: usize,
    dots: usize,
    dashes: usize,
    letters: usize,
    words: usize,
    estimated_duration_ms: u64,
};

/// Analyze text and its Morse code representation
pub fn analyze(allocator: std.mem.Allocator, text: []const u8, timing: Timing) MorseError!MorseStats {
    const morse = try encode(allocator, text);
    defer allocator.free(morse);

    var stats = MorseStats{
        .total_chars = text.len,
        .encodable_chars = 0,
        .dots = 0,
        .dashes = 0,
        .letters = 0,
        .words = 1,
        .estimated_duration_ms = 0,
    };

    stats.encodable_chars = countEncodable(text);

    var prev_char: u8 = 0;
    for (morse) |c| {
        switch (c) {
            '.' => {
                stats.dots += 1;
                stats.estimated_duration_ms += timing.dot_duration_ms + timing.intra_char_gap_ms;
            },
            '-' => {
                stats.dashes += 1;
                stats.estimated_duration_ms += timing.dash_duration_ms + timing.intra_char_gap_ms;
            },
            ' ' => {
                if (prev_char != '/') {
                    stats.letters += 1;
                }
                stats.estimated_duration_ms += timing.inter_char_gap_ms;
            },
            '/' => {
                stats.words += 1;
                stats.estimated_duration_ms += timing.word_gap_ms;
            },
            else => {},
        }
        prev_char = c;
    }

    // Count last letter if exists
    if (stats.dots > 0 or stats.dashes > 0) {
        stats.letters += 1;
    }

    return stats;
}

// ============================================================================
// Tests
// ============================================================================

test "encodeChar" {
    try std.testing.expectEqualSlices(u8, ".-", encodeChar('A').?);
    try std.testing.expectEqualSlices(u8, ".-", encodeChar('a').?);
    try std.testing.expectEqualSlices(u8, "-...", encodeChar('B').?);
    try std.testing.expectEqualSlices(u8, "-----", encodeChar('0').?);
    try std.testing.expectEqualSlices(u8, ".----", encodeChar('1').?);
    try std.testing.expectEqualSlices(u8, ".-.-.-", encodeChar('.').?);
    try std.testing.expect(encodeChar('`') == null);
}

test "encode basic" {
    const allocator = std.testing.allocator;

    const result = try encode(allocator, "SOS");
    defer allocator.free(result);
    try std.testing.expectEqualSlices(u8, "... --- ...", result);

    const result2 = try encode(allocator, "HELLO WORLD");
    defer allocator.free(result2);
    try std.testing.expectEqualSlices(u8, ".... . .-.. .-.. --- / .-- --- .-. .-.. -..", result2);

    const result3 = try encode(allocator, "123");
    defer allocator.free(result3);
    try std.testing.expectEqualSlices(u8, ".---- ..--- ...--", result3);
}

test "decode basic" {
    const allocator = std.testing.allocator;

    const result = try decode(allocator, "... --- ...");
    defer allocator.free(result);
    try std.testing.expectEqualSlices(u8, "SOS", result);

    const result2 = try decode(allocator, ".... . .-.. .-.. --- / .-- --- .-. .-.. -..");
    defer allocator.free(result2);
    try std.testing.expectEqualSlices(u8, "HELLO WORLD", result2);
}

test "encode decode roundtrip" {
    const allocator = std.testing.allocator;

    const original = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG";
    const encoded = try encode(allocator, original);
    defer allocator.free(encoded);

    const decoded = try decode(allocator, encoded);
    defer allocator.free(decoded);

    try std.testing.expectEqualSlices(u8, original, decoded);
}

test "punctuation encoding" {
    const allocator = std.testing.allocator;

    const result = try encode(allocator, "HELLO!");
    defer allocator.free(result);
    try std.testing.expectEqualSlices(u8, ".... . .-.. .-.. --- -.-.--", result);

    const result2 = try encode(allocator, "HI?");
    defer allocator.free(result2);
    try std.testing.expectEqualSlices(u8, ".... .. ..--..", result2);
}

test "generateSignals" {
    const allocator = std.testing.allocator;
    const timing = Timing{};

    const signals = try generateSignals(allocator, ".-", timing);
    defer freeSignals(allocator, signals);

    try std.testing.expectEqual(@as(usize, 4), signals.len);
    try std.testing.expectEqual(true, signals[0].active); // dot on
    try std.testing.expectEqual(timing.dot_duration_ms, signals[0].duration_ms);
    try std.testing.expectEqual(false, signals[1].active); // gap
    try std.testing.expectEqual(true, signals[2].active); // dash on
    try std.testing.expectEqual(timing.dash_duration_ms, signals[2].duration_ms);
}

test "countSymbols" {
    const symbols = countSymbols("... --- ...");
    try std.testing.expectEqual(@as(usize, 6), symbols.dots);
    try std.testing.expectEqual(@as(usize, 3), symbols.dashes);
}

test "isEncodable" {
    try std.testing.expect(isEncodable('A'));
    try std.testing.expect(isEncodable('z'));
    try std.testing.expect(isEncodable('0'));
    try std.testing.expect(isEncodable('9'));
    try std.testing.expect(isEncodable('.'));
    try std.testing.expect(!isEncodable('~'));
    try std.testing.expect(!isEncodable('`'));
}

test "isValidMorse" {
    try std.testing.expect(isValidMorse(".- -... -.-."));
    try std.testing.expect(isValidMorse("... --- ... / .-"));
    try std.testing.expect(!isValidMorse(".- x .-"));
    try std.testing.expect(!isValidMorse(".-abc"));
}

test "cleanMorse" {
    const allocator = std.testing.allocator;

    const result = try cleanMorse(allocator, ".- x .-");
    defer allocator.free(result);
    try std.testing.expectEqualSlices(u8, ".-  .-", result);
}

test "formatVisual" {
    const allocator = std.testing.allocator;

    const result = try formatVisual(allocator, ".-", '*', '-');
    defer allocator.free(result);
    try std.testing.expectEqualSlices(u8, "*-", result);
}

test "analyze" {
    const allocator = std.testing.allocator;
    const timing = Timing{};

    const stats = try analyze(allocator, "SOS", timing);

    try std.testing.expectEqual(@as(usize, 3), stats.total_chars);
    try std.testing.expectEqual(@as(usize, 3), stats.encodable_chars);
    try std.testing.expectEqual(@as(usize, 6), stats.dots);
    try std.testing.expectEqual(@as(usize, 3), stats.dashes);
    try std.testing.expectEqual(@as(usize, 3), stats.letters);
    try std.testing.expectEqual(@as(usize, 1), stats.words);
}

test "encodeSOS" {
    const allocator = std.testing.allocator;

    const result = try encodeSOS(allocator);
    defer allocator.free(result);
    try std.testing.expectEqualSlices(u8, "... --- ...", result);
}

test "encodeWithSeparator" {
    const allocator = std.testing.allocator;

    const result = try encodeWithSeparator(allocator, "HELLO WORLD", " | ");
    defer allocator.free(result);
    try std.testing.expectEqualSlices(u8, ".... . .-.. .-.. --- | .-- --- .-. .-.. -..", result);
}

test "calculateDuration" {
    const timing = Timing{
        .dot_duration_ms = 100,
        .dash_duration_ms = 300,
        .intra_char_gap_ms = 100,
        .inter_char_gap_ms = 300,
        .word_gap_ms = 700,
    };

    // ".-" = dot(100) + gap(100) + dash(300) + gap(100) = 600
    const duration = calculateDuration(".-", timing);
    try std.testing.expectEqual(@as(u64, 600), duration);
}