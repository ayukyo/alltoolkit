const std = @import("std");
const bip39 = @import("bip39_utils.zig");

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    std.debug.print("\n=== BIP39 Utils 示例 ===\n\n", .{});

    // 1. 生成不同长度的助记词
    std.debug.print("1. 生成助记词:\n", .{});
    
    std.debug.print("   12 词助记词: ", .{});
    const mnemonic12 = try bip39.generateMnemonic(allocator, bip39.EntropyBits.bits_128);
    std.debug.print("{s}\n", .{mnemonic12});

    std.debug.print("   15 词助记词: ", .{});
    const mnemonic15 = try bip39.generateMnemonic(allocator, bip39.EntropyBits.bits_160);
    std.debug.print("{s}\n", .{mnemonic15});

    std.debug.print("   24 词助记词: ", .{});
    const mnemonic24 = try bip39.generateMnemonic(allocator, bip39.EntropyBits.bits_256);
    std.debug.print("{s}\n", .{mnemonic24});

    std.debug.print("\n", .{});

    // 2. 验证助记词
    std.debug.print("2. 验证助记词:\n", .{});
    
    const is_valid12 = bip39.validateMnemonic(mnemonic12);
    std.debug.print("   12 词助记词有效: {}\n", .{is_valid12});

    const is_valid24 = bip39.validateMnemonic(mnemonic24);
    std.debug.print("   24 词助记词有效: {}\n", .{is_valid24});

    // 测试无效助记词
    const invalid_mnemonic = "invalid words that do not exist in bip39";
    const is_invalid_valid = bip39.validateMnemonic(invalid_mnemonic);
    std.debug.print("   无效助记词验证: {}\n", .{is_invalid_valid});

    std.debug.print("\n", .{});

    // 3. 获取助记词信息
    std.debug.print("3. 获取助记词信息:\n", .{});
    
    const info12 = bip39.getMnemonicInfo(mnemonic12);
    std.debug.print("   12 词助记词信息:\n", .{});
    std.debug.print("     词数: {}\n", .{info12.word_count});
    std.debug.print("     熵位数: {}\n", .{info12.entropy_bits});
    std.debug.print("     校验位数: {}\n", .{info12.checksum_bits});
    std.debug.print("     有效性: {}\n", .{info12.is_valid});

    std.debug.print("\n", .{});

    // 4. 生成种子
    std.debug.print("4. 生成种子:\n", .{});
    
    // 无密码短语
    const seed_no_passphrase = try bip39.mnemonicToSeed(allocator, mnemonic12, "");
    const seed_hex_no = try bip39.formatSeedHex(allocator, seed_no_passphrase);
    std.debug.print("   无密码短语种子 (前32字节):\n", .{});
    std.debug.print("     {s}\n", .{seed_hex_no[0..32]});
    std.debug.print("     {s}\n", .{seed_hex_no[32..64]});

    // 有密码短语
    const passphrase = "hello world";
    const seed_with_passphrase = try bip39.mnemonicToSeed(allocator, mnemonic12, passphrase);
    const seed_hex_with = try bip39.formatSeedHex(allocator, seed_with_passphrase);
    std.debug.print("   有密码短语种子 (前32字节):\n", .{});
    std.debug.print("     {s}\n", .{seed_hex_with[0..32]});
    std.debug.print("     {s}\n", .{seed_hex_with[32..64]});

    std.debug.print("\n", .{});

    // 5. 单词查询
    std.debug.print("5. 单词查询:\n", .{});
    
    std.debug.print("   前10个单词:\n", .{});
    for (0..10) |i| {
        const word = bip39.getWord(@intCast(i));
        std.debug.print("     {}: {s}\n", .{ i, word.? });
    }

    std.debug.print("\n", .{});

    // 6. 熵操作
    std.debug.print("6. 熵操作:\n", .{});
    
    // 生成熵
    const entropy = try bip39.generateEntropy(allocator, bip39.EntropyBits.bits_128);
    std.debug.print("   生成的熵 (16字节):\n", .{});
    
    var entropy_hex = try allocator.alloc(u8, entropy.len * 2);
    const hex_chars = "0123456789abcdef";
    for (entropy, 0..) |byte, i| {
        entropy_hex[i * 2] = hex_chars[byte >> 4];
        entropy_hex[i * 2 + 1] = hex_chars[byte & 0x0F];
    }
    std.debug.print("     {s}\n", .{entropy_hex});

    // 熵转助记词
    const mnemonic_from_entropy = try bip39.entropyToMnemonic(allocator, entropy);
    std.debug.print("   熵转助记词: {s}\n", .{mnemonic_from_entropy});

    std.debug.print("\n", .{});

    // 7. 辅助函数演示
    std.debug.print("7. 辅助函数:\n", .{});
    
    const word_count = bip39.getMnemonicWordCount(mnemonic12);
    std.debug.print("   词数统计: {}\n", .{word_count});

    const entropy_bits = bip39.entropyBitsFromWordCount(12);
    std.debug.print("   12词对应熵位数: {} bits\n", .{entropy_bits.?});

    std.debug.print("\n=== 演示完成 ===\n\n", .{});
}