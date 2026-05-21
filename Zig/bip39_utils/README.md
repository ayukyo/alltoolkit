# BIP39 Utils - Zig

BIP39 助记词工具库，用于生成、验证和转换 BIP39 助记词。

## 功能

- **助记词生成** - 支持生成 12/15/18/21/24 个词的助记词
- **助记词验证** - 验证助记词的有效性和校验和
- **熵转换** - 熵到助记词、助记词到熵的双向转换
- **种子生成** - 使用 PBKDF2-HMAC-SHA512 生成 64 字节种子
- **信息查询** - 获取助记词详细信息

## 使用示例

```zig
const std = @import("std");
const bip39 = @import("bip39_utils.zig");

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    // 1. 生成 12 词助记词
    const mnemonic = try bip39.generateMnemonic(allocator, bip39.EntropyBits.bits_128);
    std.debug.print("生成的助记词: {s}\n", .{mnemonic});

    // 2. 验证助记词
    const is_valid = bip39.validateMnemonic(mnemonic);
    std.debug.print("助记词有效性: {}\n", .{is_valid});

    // 3. 获取助记词信息
    const info = bip39.getMnemonicInfo(mnemonic);
    std.debug.print("词数: {}, 熵位数: {}, 校验位数: {}\n", .{
        info.word_count,
        info.entropy_bits,
        info.checksum_bits
    });

    // 4. 生成种子（带密码短语）
    const passphrase = "my passphrase";
    const seed = try bip39.mnemonicToSeed(allocator, mnemonic, passphrase);
    const seed_hex = try bip39.formatSeedHex(allocator, seed);
    std.debug.print("种子 (hex): {s}\n", .{seed_hex});

    // 5. 熵转换
    const entropy = try bip39.generateEntropy(allocator, bip39.EntropyBits.bits_128);
    const mnemonic2 = try bip39.entropyToMnemonic(allocator, entropy);
    std.debug.print("熵转助记词: {s}\n", .{mnemonic2});

    // 6. 单词验证
    std.debug.print("单词索引: {}\n", .{bip39.getWordIndex("abandon")});
    std.debug.print("索引单词: {s}\n", .{bip39.getWord(0).?});
}
```

## API 参考

### 熵位枚举

```zig
pub const EntropyBits = enum(u16) {
    bits_128 = 128,  // 12 词
    bits_160 = 160,  // 15 词
    bits_192 = 192,  // 18 词
    bits_224 = 224,  // 21 词
    bits_256 = 256,  // 24 词
};
```

### 主要函数

| 函数 | 描述 |
|------|------|
| `generateMnemonic(allocator, bits)` | 生成助记词 |
| `validateMnemonic(mnemonic)` | 验证助记词 |
| `mnemonicToSeed(allocator, mnemonic, passphrase)` | 生成种子 |
| `mnemonicToEntropy(allocator, mnemonic)` | 助记词转熵 |
| `entropyToMnemonic(allocator, entropy)` | 熵转助记词 |
| `generateEntropy(allocator, bits)` | 生成随机熵 |
| `getWordIndex(word)` | 获取单词索引 |
| `getWord(index)` | 获取索引单词 |
| `isValidWord(word)` | 验证单词 |
| `getMnemonicInfo(mnemonic)` | 获取助记词信息 |
| `formatSeedHex(allocator, seed)` | 格式化种子为十六进制 |

### 辅助函数

| 函数 | 描述 |
|------|------|
| `getMnemonicWordCount(mnemonic)` | 获取助记词词数 |
| `entropyBitsFromWordCount(count)` | 词数转熵位数 |

## 错误类型

```zig
pub const BIP39Error = error{
    InvalidEntropySize,      // 无效熵大小
    InvalidMnemonicLength,   // 无效助记词长度
    InvalidWord,             // 无效单词
    InvalidChecksum,         // 无效校验和
    InsufficientBuffer,      // 缓冲区不足
    InvalidWordIndex,        // 无效单词索引
    InvalidPassphrase,       // 无效密码短语
    RandomGenerationFailed,  // 随机生成失败
};
```

## 安全考虑

- 使用 Zig 标准库的 `std.crypto.random` 生成安全随机数
- PBKDF2 使用 2048 次迭代确保种子安全性
- 完整校验和验证防止助记词错误

## 测试

```bash
zig test bip39_utils.zig
```

## 许可证

MIT