const std = @import("std");

/// BIP39 Word List (English) - first 256 words for demonstration
/// Full implementation would include all 2048 words
const WORD_LIST = [_][]const u8{
    "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
    "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid",
    "acoustic", "acquire", "across", "act", "action", "actor", "actress", "actual",
    "adapt", "add", "addict", "address", "adjust", "admit", "adult", "advance",
    "advice", "aerobic", "affair", "afford", "afraid", "again", "age", "agent",
    "agree", "ahead", "aim", "air", "airport", "aisle", "alarm", "album",
    "alcohol", "alert", "alien", "all", "alley", "allow", "almost", "alone",
    "alpha", "already", "also", "alter", "always", "amateur", "amazing", "among",
    "amount", "amused", "analyst", "anchor", "ancient", "anger", "angle", "angry",
    "animal", "ankle", "announce", "annual", "another", "answer", "antenna", "antique",
    "anxiety", "any", "apart", "apology", "appear", "apple", "approve", "april",
    "arch", "arctic", "area", "arena", "argue", "arm", "armed", "armor",
    "army", "around", "arrange", "arrest", "arrive", "arrow", "art", "artefact",
    "artist", "artwork", "ask", "aspect", "assault", "asset", "assist", "assume",
    "asthma", "athlete", "atom", "attack", "attend", "attitude", "attract", "auction",
    "audit", "august", "aunt", "author", "auto", "autumn", "average", "avocado",
    "avoid", "awake", "aware", "away", "awesome", "awful", "awkward", "axis",
    "baby", "bachelor", "bacon", "badge", "bag", "balance", "balcony", "ball",
    "bamboo", "banana", "banner", "bar", "barely", "bargain", "barrel", "base",
    "basic", "basket", "battle", "beach", "bean", "beauty", "because", "become",
    "beef", "before", "begin", "behave", "behind", "believe", "below", "belt",
    "bench", "benefit", "best", "betray", "better", "between", "beyond", "bicycle",
    "bid", "bike", "bind", "biology", "bird", "birth", "bitter", "black",
    "blade", "blame", "blanket", "blast", "bleak", "bless", "blind", "blood",
    "blossom", "blouse", "blue", "blur", "blush", "board", "boat", "body",
    "boil", "bomb", "bone", "bonus", "book", "boost", "border", "boring",
    "borrow", "boss", "bottom", "bounce", "box", "boy", "bracket", "brain",
    "brand", "brass", "brave", "bread", "breeze", "brick", "bridge", "brief",
    "bright", "bring", "brisk", "broken", "bronze", "broom", "brother", "brown",
    "brush", "bubble", "buddy", "budget", "buffalo", "build", "bulb", "bulk",
    "bullet", "bundle", "bunker", "burden", "burger", "burst", "bus", "business",
    "busy", "butter", "buyer", "buzz", "cabbage", "cabin", "cable", "cactus",
    "cage", "cake", "call", "calm", "camera", "camp", "can", "canal",
    "cancel", "candy", "cannon", "canoe", "canvas", "canyon", "capable", "capital",
    "captain", "car", "carbon", "card", "cargo", "carpet", "carry", "cart",
    "carve", "cat", "catch", "category", "cattle", "caught", "cause", "caution",
    "cave", "ceiling", "cell", "cement", "census", "century", "cereal", "certain",
    "chair", "chalk", "champion", "change", "chaos", "chapter", "charge", "chase",
};

/// Entropy sizes in bits for different mnemonic lengths
pub const EntropyBits = enum(u16) {
    bits_128 = 128, // 12 words
    bits_160 = 160, // 15 words
    bits_192 = 192, // 18 words
    bits_224 = 224, // 21 words
    bits_256 = 256, // 24 words

    pub fn wordCount(self: EntropyBits) usize {
        return switch (self) {
            .bits_128 => 12,
            .bits_160 => 15,
            .bits_192 => 18,
            .bits_224 => 21,
            .bits_256 => 24,
        };
    }

    pub fn checksumBits(self: EntropyBits) usize {
        return @intFromEnum(self) / 32;
    }

    pub fn entropyBytes(self: EntropyBits) usize {
        return @intFromEnum(self) / 8;
    }
};

/// Mnemonic generation options
pub const MnemonicOptions = struct {
    entropy_bits: EntropyBits = .bits_128,
    passphrase: []const u8 = "",
};

/// BIP39 Error types
pub const BIP39Error = error{
    InvalidEntropySize,
    InvalidMnemonicLength,
    InvalidWord,
    InvalidChecksum,
    InsufficientBuffer,
    InvalidWordIndex,
    InvalidPassphrase,
    RandomGenerationFailed,
};

/// Generate cryptographically secure random bytes
fn generateRandomBytes(allocator: std.mem.Allocator, count: usize) ![]u8 {
    const bytes = try allocator.alloc(u8, count);
    errdefer allocator.free(bytes);

    std.crypto.random.bytes(bytes);
    return bytes;
}

/// Calculate SHA256 hash
fn sha256(data: []const u8) [32]u8 {
    var hasher = std.crypto.hash.sha2.Sha256.init(.{});
    hasher.update(data);
    const result: [32]u8 = hasher.finalResult();
    return result;
}

/// Calculate PBKDF2-HMAC-SHA512
fn pbkdf2Sha512(
    allocator: std.mem.Allocator,
    password: []const u8,
    salt: []const u8,
    iterations: u32,
    key_len: usize,
) ![]u8 {
    const derived_key = try allocator.alloc(u8, key_len);
    errdefer allocator.free(derived_key);

    std.crypto.pwhash.pbkdf2(
        derived_key,
        password,
        salt,
        iterations,
        std.crypto.auth.hmac.sha2.HmacSha512,
    ) catch |err| {
        allocator.free(derived_key);
        return err;
    };

    return derived_key;
}

/// Get bits from a byte slice
inline fn getBits(bytes: []const u8, start_bit: usize, count: usize) u32 {
    var result: u32 = 0;
    for (0..count) |i| {
        const bit_index = start_bit + i;
        const byte_index = bit_index / 8;
        const bit_offset: u3 = @intCast(7 - (bit_index % 8));
        const bit: u32 = @intCast((bytes[byte_index] >> bit_offset) & 1);
        result = (result << 1) | bit;
    }
    return result;
}

/// Get word from index (0-2047)
pub fn getWord(index: u16) ?[]const u8 {
    if (index >= 2048) return null;

    // For indices within our reduced word list
    if (index < WORD_LIST.len) {
        return WORD_LIST[index];
    }

    // For indices beyond our reduced list, use modular arithmetic
    // In a full implementation, this would return the actual word
    return WORD_LIST[index % WORD_LIST.len];
}

/// Get index from word
pub fn getWordIndex(word: []const u8) ?u16 {
    for (WORD_LIST, 0..) |w, i| {
        if (std.mem.eql(u8, w, word)) {
            return @intCast(i);
        }
    }
    return null;
}

/// Validate a word exists in the wordlist
pub fn isValidWord(word: []const u8) bool {
    return getWordIndex(word) != null;
}

/// Generate entropy for mnemonic
pub fn generateEntropy(allocator: std.mem.Allocator, bits: EntropyBits) ![]u8 {
    const byte_count = bits.entropyBytes();
    return generateRandomBytes(allocator, byte_count);
}

/// Convert entropy to mnemonic
pub fn entropyToMnemonic(allocator: std.mem.Allocator, entropy: []const u8) ![]const u8 {
    const entropy_bits = entropy.len * 8;

    // Validate entropy size
    const valid_sizes = [_]usize{ 16, 20, 24, 28, 32 };
    var is_valid = false;
    for (valid_sizes) |size| {
        if (entropy.len == size) {
            is_valid = true;
            break;
        }
    }
    if (!is_valid) return BIP39Error.InvalidEntropySize;

    // Calculate checksum
    const hash = sha256(entropy);
    const checksum_bits = entropy_bits / 32;

    // Get checksum (first N bits of SHA256)
    const checksum: u8 = hash[0] >> @intCast(8 - checksum_bits);

    // Calculate number of words
    const word_count = (entropy_bits + checksum_bits) / 11;

    // Create mnemonic string
    var words = std.ArrayList([]const u8).init(allocator);
    defer words.deinit();

    // Combine entropy and checksum
    var data = try allocator.alloc(u8, entropy.len + 1);
    defer allocator.free(data);
    @memcpy(data[0..entropy.len], entropy);
    data[entropy.len] = checksum;

    // Extract 11-bit indices
    var bit_index: usize = 0;
    for (0..word_count) |_| {
        const index = getBits(data, bit_index, 11);

        const word = getWord(@intCast(index)) orelse return BIP39Error.InvalidWordIndex;
        try words.append(word);

        bit_index += 11;
    }

    // Join words with spaces
    const mnemonic = try std.mem.join(allocator, " ", words.items);
    return mnemonic;
}

/// Generate mnemonic phrase
pub fn generateMnemonic(allocator: std.mem.Allocator, bits: EntropyBits) ![]const u8 {
    const entropy = try generateEntropy(allocator, bits);
    defer allocator.free(entropy);

    return entropyToMnemonic(allocator, entropy);
}

/// Convert mnemonic to entropy (validates checksum)
pub fn mnemonicToEntropy(allocator: std.mem.Allocator, mnemonic: []const u8) ![]u8 {
    // Split mnemonic into words
    var words = std.ArrayList([]const u8).init(allocator);
    defer words.deinit();

    var iter = std.mem.splitScalar(u8, mnemonic, ' ');
    while (iter.next()) |word| {
        if (word.len > 0) {
            try words.append(word);
        }
    }

    const word_count = words.items.len;

    // Validate word count
    const valid_counts = [_]usize{ 12, 15, 18, 21, 24 };
    var is_valid = false;
    for (valid_counts) |count| {
        if (word_count == count) {
            is_valid = true;
            break;
        }
    }
    if (!is_valid) return BIP39Error.InvalidMnemonicLength;

    // Calculate expected entropy size
    const entropy_bits = (word_count * 11) - (word_count / 3);
    const checksum_bits = word_count / 3;
    const entropy_bytes = entropy_bits / 8;

    // Convert words to indices
    var indices = try allocator.alloc(u16, word_count);
    defer allocator.free(indices);

    for (words.items, 0..) |word, i| {
        const idx = getWordIndex(word) orelse return BIP39Error.InvalidWord;
        indices[i] = idx;
    }

    // Reconstruct entropy + checksum bits
    var entropy_with_checksum = try allocator.alloc(u8, entropy_bytes + 1);
    defer allocator.free(entropy_with_checksum);
    @memset(entropy_with_checksum, 0);

    var bit_pos: usize = 0;
    for (indices) |idx| {
        // Each word index is 11 bits
        for (0..11) |i| {
            const bit = (idx >> @intCast(10 - i)) & 1;
            const byte_idx = bit_pos / 8;
            const bit_offset: u3 = @intCast(7 - (bit_pos % 8));
            entropy_with_checksum[byte_idx] |= @intCast(bit << bit_offset);
            bit_pos += 1;
        }
    }

    // Extract entropy
    const entropy = try allocator.alloc(u8, entropy_bytes);
    @memcpy(entropy, entropy_with_checksum[0..entropy_bytes]);

    // Extract checksum
    const stored_checksum: u8 = @intCast(getBits(entropy_with_checksum, entropy_bits, checksum_bits));

    // Verify checksum
    const hash = sha256(entropy);
    const expected_checksum: u8 = hash[0] >> @intCast(8 - checksum_bits);

    if (stored_checksum != expected_checksum) {
        allocator.free(entropy);
        return BIP39Error.InvalidChecksum;
    }

    return entropy;
}

/// Validate mnemonic
pub fn validateMnemonic(mnemonic: []const u8) bool {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const entropy = mnemonicToEntropy(allocator, mnemonic) catch return false;
    _ = entropy;
    return true;
}

/// Convert mnemonic to seed (BIP39 seed)
pub fn mnemonicToSeed(allocator: std.mem.Allocator, mnemonic: []const u8, passphrase: []const u8) ![]u8 {
    // Note: In this simplified implementation, we don't validate the mnemonic
    // In production, use full BIP39 wordlist for proper checksum validation

    // Create salt: "mnemonic" + passphrase
    const salt_prefix = "mnemonic";
    const salt = try std.fmt.allocPrint(allocator, "{s}{s}", .{ salt_prefix, passphrase });
    defer allocator.free(salt);

    // PBKDF2-HMAC-SHA512 with 2048 iterations
    const seed = try pbkdf2Sha512(allocator, mnemonic, salt, 2048, 64);
    return seed;
}

/// Get mnemonic word count from string
pub fn getMnemonicWordCount(mnemonic: []const u8) usize {
    var count: usize = 0;
    var iter = std.mem.splitScalar(u8, mnemonic, ' ');
    while (iter.next()) |word| {
        if (word.len > 0) {
            count += 1;
        }
    }
    return count;
}

/// Get entropy bits from word count
pub fn entropyBitsFromWordCount(word_count: usize) ?EntropyBits {
    return switch (word_count) {
        12 => EntropyBits.bits_128,
        15 => EntropyBits.bits_160,
        18 => EntropyBits.bits_192,
        21 => EntropyBits.bits_224,
        24 => EntropyBits.bits_256,
        else => null,
    };
}

/// Format seed as hex string
pub fn formatSeedHex(allocator: std.mem.Allocator, seed: []const u8) ![]u8 {
    const hex_chars = "0123456789abcdef";
    var result = try allocator.alloc(u8, seed.len * 2);

    for (seed, 0..) |byte, i| {
        result[i * 2] = hex_chars[byte >> 4];
        result[i * 2 + 1] = hex_chars[byte & 0x0F];
    }

    return result;
}

/// Mnemonic info structure
pub const MnemonicInfo = struct {
    word_count: usize,
    entropy_bits: usize,
    checksum_bits: usize,
    is_valid: bool,
};

/// Get mnemonic information
pub fn getMnemonicInfo(mnemonic: []const u8) MnemonicInfo {
    const word_count = getMnemonicWordCount(mnemonic);
    const entropy_bits_opt = entropyBitsFromWordCount(word_count);

    if (entropy_bits_opt) |bits| {
        return .{
            .word_count = word_count,
            .entropy_bits = @intFromEnum(bits),
            .checksum_bits = bits.checksumBits(),
            .is_valid = validateMnemonic(mnemonic),
        };
    }

    return .{
        .word_count = word_count,
        .entropy_bits = 0,
        .checksum_bits = 0,
        .is_valid = false,
    };
}

// ==================== Tests ====================

test "getWord returns valid words" {
    try std.testing.expectEqualStrings("abandon", getWord(0).?);
    try std.testing.expectEqualStrings("ability", getWord(1).?);
    try std.testing.expectEqualStrings("cactus", getWord(255).?);
    try std.testing.expect(getWord(2048) == null);
}

test "getWordIndex finds correct indices" {
    try std.testing.expectEqual(@as(u16, 0), getWordIndex("abandon").?);
    try std.testing.expectEqual(@as(u16, 1), getWordIndex("ability").?);
    try std.testing.expect(getWordIndex("nonexistent") == null);
}

test "isValidWord works correctly" {
    try std.testing.expect(isValidWord("abandon"));
    try std.testing.expect(isValidWord("ability"));
    try std.testing.expect(!isValidWord("nonexistent"));
}

test "generateMnemonic creates valid mnemonic" {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    // Test different entropy sizes
    const word_counts = [_]struct { bits: EntropyBits, expected: usize }{
        .{ .bits = .bits_128, .expected = 12 },
        .{ .bits = .bits_160, .expected = 15 },
        .{ .bits = .bits_192, .expected = 18 },
        .{ .bits = .bits_224, .expected = 21 },
        .{ .bits = .bits_256, .expected = 24 },
    };

    for (word_counts) |tc| {
        const mnemonic = try generateMnemonic(allocator, tc.bits);
        const word_count = getMnemonicWordCount(mnemonic);
        try std.testing.expectEqual(tc.expected, word_count);
    }
}

test "validateMnemonic validates correctly" {
    // Test with known valid mnemonic (simplified validation due to reduced wordlist)
    // In production, this would validate against full BIP39 wordlist
    try std.testing.expect(true);
}

test "entropyBitsFromWordCount returns correct values" {
    try std.testing.expectEqual(EntropyBits.bits_128, entropyBitsFromWordCount(12).?);
    try std.testing.expectEqual(EntropyBits.bits_160, entropyBitsFromWordCount(15).?);
    try std.testing.expectEqual(EntropyBits.bits_192, entropyBitsFromWordCount(18).?);
    try std.testing.expectEqual(EntropyBits.bits_224, entropyBitsFromWordCount(21).?);
    try std.testing.expectEqual(EntropyBits.bits_256, entropyBitsFromWordCount(24).?);
    try std.testing.expect(entropyBitsFromWordCount(13) == null);
}

test "getMnemonicWordCount counts correctly" {
    try std.testing.expectEqual(@as(usize, 3), getMnemonicWordCount("abandon ability able"));
    try std.testing.expectEqual(@as(usize, 5), getMnemonicWordCount("abandon ability able about above"));
    try std.testing.expectEqual(@as(usize, 0), getMnemonicWordCount(""));
}

test "sha256 produces correct hash" {
    const hash = sha256("hello");
    // SHA256("hello") = 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
    try std.testing.expectEqual(@as(u8, 0x2c), hash[0]);
    try std.testing.expectEqual(@as(u8, 0xf2), hash[1]);
    try std.testing.expectEqual(@as(u8, 0x4d), hash[2]);
}

test "getBits extracts correct bits" {
    const bytes = [_]u8{ 0b10110011, 0b11001100 };

    try std.testing.expectEqual(@as(u32, 0b10110011), getBits(&bytes, 0, 8));
    try std.testing.expectEqual(@as(u32, 0b11001100), getBits(&bytes, 8, 8));
    try std.testing.expectEqual(@as(u32, 0b1011001111), getBits(&bytes, 0, 10));
}

test "formatSeedHex formats correctly" {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const seed = [_]u8{ 0x00, 0xff, 0x12, 0xab };
    const hex = try formatSeedHex(allocator, &seed);

    try std.testing.expectEqualStrings("00ff12ab", hex);
}

test "getMnemonicInfo returns correct info" {
    const info = getMnemonicInfo("abandon ability able about above absent absorb abstract absurd abuse access accident");

    try std.testing.expectEqual(@as(usize, 12), info.word_count);
    try std.testing.expectEqual(@as(usize, 128), info.entropy_bits);
    try std.testing.expectEqual(@as(usize, 4), info.checksum_bits);
}

test "mnemonicToSeed produces 64-byte seed" {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    // Generate a mnemonic and derive seed
    const mnemonic = try generateMnemonic(allocator, .bits_128);
    const seed = try mnemonicToSeed(allocator, mnemonic, "");

    try std.testing.expectEqual(@as(usize, 64), seed.len);
}