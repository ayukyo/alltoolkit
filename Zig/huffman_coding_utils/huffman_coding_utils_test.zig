const std = @import("std");
const huffman = @import("mod.zig");

test "完整编码解码流程 - 简单文本" {
    const allocator = std.testing.allocator;

    // 编码
    var encoder = huffman.HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    const original = "hello";
    try encoder.build(original);

    const encoded = try encoder.encode(original);
    defer allocator.free(encoded);

    // 验证编码表
    try std.testing.expect(encoder.getCode('h') != null);
    try std.testing.expect(encoder.getCode('e') != null);
    try std.testing.expect(encoder.getCode('l') != null);
    try std.testing.expect(encoder.getCode('o') != null);

    // 计算总位数
    var total_bits: usize = 0;
    for (original) |char| {
        if (encoder.getCode(char)) |code| {
            total_bits += code.len;
        }
    }

    // 解码
    var decoder = huffman.HuffmanDecoder.init(allocator);
    defer decoder.deinit();

    try decoder.buildFromCodes(encoder.getCodeTable(), allocator);
    const decoded = try decoder.decode(encoded, total_bits, allocator);
    defer allocator.free(decoded);

    try std.testing.expectEqualSlices(u8, original, decoded);
}

test "完整编码解码流程 - 重复字符" {
    const allocator = std.testing.allocator;

    var encoder = huffman.HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    const original = "aaabbbccc";
    try encoder.build(original);

    const encoded = try encoder.encode(original);
    defer allocator.free(encoded);

    // a,b,c 各出现3次，应有相近长度的编码
    const code_a = encoder.getCode('a').?;
    const code_b = encoder.getCode('b').?;
    const code_c = encoder.getCode('c').?;

    try std.testing.expect(code_a.len > 0);
    try std.testing.expect(code_b.len > 0);
    try std.testing.expect(code_c.len > 0);

    // 计算总位数
    var total_bits: usize = 0;
    for (original) |char| {
        if (encoder.getCode(char)) |code| {
            total_bits += code.len;
        }
    }

    // 解码验证
    var decoder = huffman.HuffmanDecoder.init(allocator);
    defer decoder.deinit();

    try decoder.buildFromCodes(encoder.getCodeTable(), allocator);
    const decoded = try decoder.decode(encoded, total_bits, allocator);
    defer allocator.free(decoded);

    try std.testing.expectEqualSlices(u8, original, decoded);
}

test "完整编码解码流程 - 长文本" {
    const allocator = std.testing.allocator;

    var encoder = huffman.HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    const original = "the quick brown fox jumps over the lazy dog";
    try encoder.build(original);

    const encoded = try encoder.encode(original);
    defer allocator.free(encoded);

    // 计算总位数
    var total_bits: usize = 0;
    for (original) |char| {
        if (encoder.getCode(char)) |code| {
            total_bits += code.len;
        }
    }

    // 解码
    var decoder = huffman.HuffmanDecoder.init(allocator);
    defer decoder.deinit();

    try decoder.buildFromCodes(encoder.getCodeTable(), allocator);
    const decoded = try decoder.decode(encoded, total_bits, allocator);
    defer allocator.free(decoded);

    try std.testing.expectEqualSlices(u8, original, decoded);
}

test "完整编码解码流程 - 空格和特殊字符" {
    const allocator = std.testing.allocator;

    var encoder = huffman.HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    const original = "a b c d e f g";
    try encoder.build(original);

    const encoded = try encoder.encode(original);
    defer allocator.free(encoded);

    // 计算总位数
    var total_bits: usize = 0;
    for (original) |char| {
        if (encoder.getCode(char)) |code| {
            total_bits += code.len;
        }
    }

    var decoder = huffman.HuffmanDecoder.init(allocator);
    defer decoder.deinit();

    try decoder.buildFromCodes(encoder.getCodeTable(), allocator);
    const decoded = try decoder.decode(encoded, total_bits, allocator);
    defer allocator.free(decoded);

    try std.testing.expectEqualSlices(u8, original, decoded);
}

test "频率计算测试" {
    const allocator = std.testing.allocator;

    const data = "aabbcc";
    var freq = try huffman.calculateFrequency(allocator, data);
    defer freq.deinit();

    try std.testing.expectEqual(@as(usize, 2), freq.get('a').?);
    try std.testing.expectEqual(@as(usize, 2), freq.get('b').?);
    try std.testing.expectEqual(@as(usize, 2), freq.get('c').?);
}

test "压缩率计算测试" {
    // 100 字节原始数据，编码后 400 位 = 50 字节
    const ratio = huffman.calculateCompressionRatio(100, 400);
    try std.testing.expectApproxEqAbs(@as(f64, 50.0), ratio, 0.01);

    // 无压缩
    const no_compression = huffman.calculateCompressionRatio(100, 800);
    try std.testing.expectApproxEqAbs(@as(f64, 0.0), no_compression, 0.01);
}

test "高频字符获得更短编码" {
    const allocator = std.testing.allocator;

    var encoder = huffman.HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    // 'a' 出现 10 次，'b' 出现 1 次
    const original = "aaaaaaaaa b";
    try encoder.build(original);

    const code_a = encoder.getCode('a').?;
    const code_b = encoder.getCode('b').?;

    // 高频字符应该有更短的编码
    try std.testing.expect(code_a.len <= code_b.len);
}

test "二进制数据编码" {
    const allocator = std.testing.allocator;

    var encoder = huffman.HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    const original = [_]u8{ 0x00, 0x01, 0x02, 0x00, 0x01, 0x00 };
    try encoder.build(&original);

    const encoded = try encoder.encode(&original);
    defer allocator.free(encoded);

    try std.testing.expect(encoded.len > 0);
}

test "大量重复字符" {
    const allocator = std.testing.allocator;

    var encoder = huffman.HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    const original = [_]u8{'a'} ** 1000;
    try encoder.build(&original);

    const encoded = try encoder.encode(&original);
    defer allocator.free(encoded);

    // 单字符应该压缩得非常小
    // 单字符编码长度应该是 1 位，1000 位 = 125 字节
    try std.testing.expect(encoded.len <= 125);
}

test "编码解码 - 数字和字母混合" {
    const allocator = std.testing.allocator;

    var encoder = huffman.HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    const original = "abc123ABC";
    try encoder.build(original);

    const encoded = try encoder.encode(original);
    defer allocator.free(encoded);

    // 计算总位数
    var total_bits: usize = 0;
    for (original) |char| {
        if (encoder.getCode(char)) |code| {
            total_bits += code.len;
        }
    }

    var decoder = huffman.HuffmanDecoder.init(allocator);
    defer decoder.deinit();

    try decoder.buildFromCodes(encoder.getCodeTable(), allocator);
    const decoded = try decoder.decode(encoded, total_bits, allocator);
    defer allocator.free(decoded);

    try std.testing.expectEqualSlices(u8, original, decoded);
}

test "单一字符编码解码" {
    const allocator = std.testing.allocator;

    var encoder = huffman.HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    const original = "x";
    try encoder.build(original);

    const encoded = try encoder.encode(original);
    defer allocator.free(encoded);

    // 计算总位数
    var total_bits: usize = 0;
    for (original) |char| {
        if (encoder.getCode(char)) |code| {
            total_bits += code.len;
        }
    }

    var decoder = huffman.HuffmanDecoder.init(allocator);
    defer decoder.deinit();

    try decoder.buildFromCodes(encoder.getCodeTable(), allocator);
    const decoded = try decoder.decode(encoded, total_bits, allocator);
    defer allocator.free(decoded);

    try std.testing.expectEqualSlices(u8, original, decoded);
}

test "单一字符重复编码解码" {
    const allocator = std.testing.allocator;

    var encoder = huffman.HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    const original = "xxxxx";
    try encoder.build(original);

    const encoded = try encoder.encode(original);
    defer allocator.free(encoded);

    // 计算总位数
    var total_bits: usize = 0;
    for (original) |char| {
        if (encoder.getCode(char)) |code| {
            total_bits += code.len;
        }
    }

    var decoder = huffman.HuffmanDecoder.init(allocator);
    defer decoder.deinit();

    try decoder.buildFromCodes(encoder.getCodeTable(), allocator);
    const decoded = try decoder.decode(encoded, total_bits, allocator);
    defer allocator.free(decoded);

    try std.testing.expectEqualSlices(u8, original, decoded);
}

test "编码表一致性" {
    const allocator = std.testing.allocator;

    var encoder = huffman.HuffmanEncoder.init(allocator);
    defer encoder.deinit();

    const original = "abacabad";
    try encoder.build(original);

    // 验证编码表的前缀性质（无编码是另一个编码的前缀）
    const codes = encoder.getCodeTable();
    var iter1 = codes.iterator();
    while (iter1.next()) |entry1| {
        var iter2 = codes.iterator();
        while (iter2.next()) |entry2| {
            if (entry1.key_ptr.* != entry2.key_ptr.*) {
                const code1 = entry1.value_ptr.*;
                const code2 = entry2.value_ptr.*;
                // 检查 code1 不是 code2 的前缀
                if (code1.len < code2.len) {
                    try std.testing.expect(!std.mem.startsWith(u8, code2, code1));
                }
            }
        }
    }
}